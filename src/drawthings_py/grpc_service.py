"""gRPC client helper for DrawThings image generation service.

This module provides `GrpcService`, a thin wrapper around the
generated gRPC stub for streaming image generation responses.

It exposes a single async method, `generate_image`, which yields
progress via an optional preview callback and collects generated
image tensors into `ImageBuffer` instances.
"""

import os
import ssl
from grpclib.client import Channel
import tqdm

from drawthings_py.generated.dt_grpc.image_service import ImageGenerationSignpostProto
from drawthings_py.metadata import _with_seed, create_metadata

from .generated.dt_grpc.GenerationConfiguration import GenerationConfiguration
from .image_buffer import ImageBuffer
from .drawthings_service import DrawThingsService
from .request_builder import RequestBuilder, _build_message
from .grpc import image_service
from .preview_decoders import decode_preview
from ._util import pluralize, seeds_from_batch

cert_path = os.path.join(os.path.dirname(__file__), "root_ca.crt")
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.load_verify_locations(cafile=cert_path)
ssl_context.check_hostname = False
ssl_context.set_alpn_protocols(["h2"])


def format_signpost(msg) -> str:
    if msg.is_set("text_encoded"):
        return "Text encoded"

    if msg.is_set("image_encoded"):
        return "Image encoded"

    if msg.is_set("sampling"):
        return f"Sampling: step {msg.sampling.step}"

    if msg.is_set("image_decoded"):
        return "Image decoded"

    if msg.is_set("second_pass_image_encoded"):
        return "Second pass encoding"

    if msg.is_set("second_pass_sampling"):
        return f"Second pass sampling: step {msg.second_pass_sampling.step}"

    if msg.is_set("second_pass_image_decoded"):
        return "Second pass decoded"

    if msg.is_set("face_restored"):
        return "Face restored"

    if msg.is_set("image_upscaled"):
        return "Image upscaled"

    return ""


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

        Progress updates and preview images can be received by attaching a callback
        to the RequestBuilder.

        Returns:
            A list of `ImageBuffer` instances created from tensors sent
            by the server. For videos, each frame is returned as a separate `ImageBuffer`.
        """
        req, on_progress = _build_message(request)

        # in order to generate metadata we need to decode the config that we used
        config = GenerationConfiguration.GetRootAs(req.configuration)
        seeds = seeds_from_batch(config.Seed(), config.BatchSize(), config.SeedMode())
        metadata = create_metadata(
            config,
            req.prompt,
            req.negative_prompt,
        )
        metadata_batch = [_with_seed(metadata, seed) for seed in seeds]

        generated_images = []
        signposts = []

        self.printStart(req)

        t = tqdm.tqdm(
            desc="Generating",
            total=config.Steps() + 5,
            ncols=80
        )

        async for response in self._service.generate_image(req):
            signpost = None
            preview = None
            if response.current_signpost is not None:
                signpost = response.current_signpost
                signpost_text = format_signpost(signpost)
                t.update(1)
                t.set_postfix_str(signpost_text)
                signposts.append(signpost_text)
            if response.preview_image is not None:
                preview = response.preview_image
            if response.generated_images:
                generated_images.extend(response.generated_images)
                t.update(1)

            if on_progress is not None:
                if signpost is not None or preview is not None:
                    on_progress(
                        signpost,
                        decode_preview(preview) if preview is not None else None,
                    )

        t.close()

        if len(generated_images) == 0:
            raise RuntimeError("No images received from server")

        result = []
        is_video = False

        if len(generated_images) != len(metadata_batch):
            # we can assume this is a video. batch size is ignored for video models
            # there is an edge case where the ignored batch_size equals number of frames
            # figure that out later
            is_video = True

        for i, image in enumerate(generated_images):
            image_metadata = metadata if is_video else metadata_batch[i]
            result.append(ImageBuffer.from_tensor(image, metadata=image_metadata))
        return result

    async def _dispose(self):
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
