"""gRPC client helper for DrawThings image generation service.

This module provides `GrpcService`, a thin wrapper around the
generated gRPC stub for streaming image generation responses.

It exposes a single async method, `generate_image`, which yields
progress via an optional preview callback and collects generated
image tensors into `ImageBuffer` instances.

The module also configures a local `ssl_context` used when creating
the gRPC `Channel`. The context is intentionally permissive here
(hostname checking disabled and `CERT_NONE`) because it's intended
for local/private development against a dev server. Do not use this
pattern in production without tightening verification.
"""

import os
import ssl
from grpclib.client import Channel
from .image_buffer import ImageBuffer
from .drawthings_service import DrawThingsService
from .request_builder import RequestBuilder, _build_message
from .generated.dt_grpc import image_service
from .preview_decoders import decode_preview
from .helpers import pluralize

# Path to a bundled root CA certificate (optional; may be absent).
cert_path = os.path.join(os.path.dirname(__file__), "root_ca.crt")
# Create an SSL context configured for HTTP/2 (used by grpclib).
# NOTE: This context disables hostname checking and certificate
# verification for convenience in development. Replace with stricter
# settings for production use.
ssl_context = ssl.create_default_context(cafile=cert_path)
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
ssl_context.set_alpn_protocols(["h2"])


class GrpcService(DrawThingsService):
    """Client wrapper around the generated ImageGenerationService stub.

    This class manages a `grpclib` `Channel` and exposes a single
    async method `generate_image` which streams responses from the
    server. It converts received image tensors into `ImageBuffer`
    objects before returning them.
    """

    _channel: Channel
    _service: image_service.ImageGenerationServiceStub

    def __init__(self, host: str = "127.0.0.1", port: int = 7859):
        """Create a `GrpcService` connected to `host:port`.

        Args:
            host: Hostname or IP of the DrawThings gRPC server.
            port: TCP port for the gRPC server.
        """
        self._channel = Channel(host, port, ssl=ssl_context)
        self._service = image_service.ImageGenerationServiceStub(self._channel)

    async def generate_image(self, request: RequestBuilder) -> list[ImageBuffer]:
        """Send a generation request and collect generated images.

        The provided `RequestBuilder` is converted into a generated
        `ImageGenerationRequest` using the module-level `_build_message`.

        The generator may stream multiple intermediate responses. If
        the `RequestBuilder` included a preview callback, it will be
        invoked with each decoded preview and the message index.

        Returns:
            A list of `ImageBuffer` instances created from tensors sent
            by the server.
        """
        req, on_preview = _build_message(request)

        current_message = 0
        generated_images = []

        self.printStart(req)
        async for response in self._service.generate_image(req):
            current_message += 1
            if response.current_signpost is not None:
                print(
                    f"Signpost: {response.current_signpost} - Message: {current_message}"
                )
            if response.preview_image and on_preview is not None:
                preview_image = decode_preview(response.preview_image, None)
                on_preview(preview_image, current_message)
            if response.generated_images:
                generated_images.extend(response.generated_images)
                print(
                    f"Received {len(response.generated_images)} {pluralize(len(response.generated_images), 'image')}!"
                )

        return [ImageBuffer.from_tensor(i) for i in generated_images]

    def dispose(self):
        """Close the underlying gRPC channel.

        Call this when the service is no longer needed to release
        network resources.
        """
        self._channel.close()

    def printStart(self, req: image_service.ImageGenerationRequest):
        """Print a concise summary of what will be sent to the server.

        The helper inspects the request for an init image, hints, and
        mask information and prints a human-friendly message.
        """
        base = "Sending generation request"
        items = []
        if req.image is not None:
            items.append("init image")
        if req.hints is not None and len(req.hints):
            total_hints = sum([len(h.tensors) for h in req.hints])
            items.append(f"{total_hints} additional {pluralize(total_hints, 'image')}")
        if req.mask is not None:
            items.append("mask")
        if len(items) > 1:
            items_text = ", ".join(items[:-1]) + " and " + items[-1]
        else:
            items_text = items[0] if len(items) else ""
        if items_text:
            message = base + " with " + items_text + "..."
        else:
            message = base + "..."
        print(message)
