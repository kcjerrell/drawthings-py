"""
gRPC client helper for DrawThings image generation service.

This module provides `GrpcService`, a thin wrapper around the
generated gRPC stub for streaming image generation responses.

It exposes a single async method, `generate_image`, which yields
progress via an optional preview callback and collects generated
image tensors into `ImageBuffer` instances.
"""

from __future__ import annotations
import math
import ssl
from importlib.resources import files
from typing import cast
from typing_extensions import override

import tqdm
from grpclib import GRPCError
from grpclib.client import Channel

from drawthings_py.grpc.audio import AudioBuffer, get_sample_rate
from drawthings_py.image_generation_result import ImageGenerationResult
from drawthings_py.models.types import ModelsInfo

from drawthings_py._dt_service import DrawThingsService
from drawthings_py.util._errors import raise_grpc_error
from drawthings_py.image._metadata import ImageMetadata, copy_with_seed, create_metadata
from drawthings_py.image._preview_decoders import decode_preview
from drawthings_py.util._util import pluralize, seeds_from_batch
from drawthings_py.generated.dt_grpc.config_generated import GenerationConfiguration
from drawthings_py.generated.dt_grpc import image_service
from drawthings_py.image.image_buffer import ImageBuffer
from drawthings_py.request_builder import (
    ProgressCallback,
    RequestBuilder,
    build_grpc_message,
)

cert_path = files("drawthings_py.resources").joinpath("root_ca.crt")
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.load_verify_locations(cafile=str(cert_path))
ssl_context.check_hostname = False
ssl_context.set_alpn_protocols(["h2"])


def format_signpost(msg: image_service.ImageGenerationSignpostProto) -> str:
    """
    Format a signpost message from a GenerationResponse.

    Args:
        msg: GenerationResponse message

    Returns:
        Formatted signpost string
    """
    if msg.is_set("text_encoded"):
        return "Text encoded"

    if msg.is_set("image_encoded"):
        return "Image encoded"

    if msg.is_set("sampling"):
        return f"Sampling: step {msg.sampling.step}"

    if msg.is_set("image_decoded"):
        return "Image decoded"

    if msg.is_set("second_pass_image_encoded"):
        return "2nd pass encoding"

    if msg.is_set("second_pass_sampling"):
        return f"2nd pass: step {msg.second_pass_sampling.step}"

    if msg.is_set("second_pass_image_decoded"):
        return "2nd pass decoded"

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

    _host: str
    _port: int
    _progressbar: bool
    _disable_messages: bool

    _channel: Channel | None
    _service: image_service.ImageGenerationServiceStub | None
    _models: ModelsInfo | None

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 7859,
        progressbar: bool = True,
        disable_messages: bool = False,
    ):
        """Create a `GrpcService` connected to `host:port`.

        Args:
            host: Hostname or IP of the DrawThings gRPC server.
            port: TCP port for the gRPC server.
            progressbar: Whether to show a progress bar during generation. (default: True)
            disable_messages: Whether to disable messages when a request is sent/completed. (default: False)
        """
        super().__init__()

        self._host = host
        self._port = port
        self._progressbar = progressbar
        self._disable_messages = disable_messages

        self._channel = None
        self._service = None
        self._models = None

    @override
    async def connect(self):
        """
        Connect to the gRPC server.

        This method is called automatically when used in an 'async with' block, or when calling
        any methods that depend on the grpc channel.
        """
        if self._channel is None:
            try:
                self._channel = Channel(self._host, self._port, ssl=ssl_context)
                self._service = image_service.ImageGenerationServiceStub(self._channel)
                await self._fetch_models()
            except Exception as e:
                # Clean up partially-initialized state so connect() can be retried
                if self._channel is not None:
                    self._channel.close()
                self._channel = None
                self._service = None
                print(f"Error connecting to gRPC server: {e}")
                raise

    async def _ensure_service(self) -> image_service.ImageGenerationServiceStub:
        """Ensures the grpc service is connected and is not None"""
        await self.connect()
        if self._service is None:
            raise RuntimeError("Service not connected")
        return self._service

    @override
    async def close(self):
        """
        Close the gRPC channel.

        Call this when the service is no longer needed to release network resources.
        This method is called automatically when used in an 'async with' block
        """
        if self._channel is not None:
            self._channel.close()
            self._channel = None
            self._service = None
            self._models = None

    @override
    async def get_models(self, refresh_cache: bool = False) -> ModelsInfo:
        """
        Get the (cached) list of models and files from the service
        args:
            refresh_cache: Whether to refresh the cache
        """
        if self._models is not None and not refresh_cache:
            return self._models
        await self._fetch_models()
        return self._models if self._models is not None else ModelsInfo()

    async def _fetch_models(self):
        service = await self._ensure_service()
        echo = await service.echo(image_service.EchoRequest("drawthings-py"))
        self._models = ModelsInfo.from_echo_reply(echo)

    @override
    async def generate_image(self, request: RequestBuilder) -> ImageGenerationResult:
        """
        Send a generation request and collect generated images.

        Progress updates and preview images can be received by attaching a callback
        to the RequestBuilder.

        Returns:
            The generated image(s), as a list of ImageBuffers
            For videos, each frame is returned as a separate `ImageBuffer`.
        """
        await self.connect()
        if self._service is None:
            raise RuntimeError("Service not connected")

        req, on_progress = build_grpc_message(request)

        # in order to generate metadata we need to decode the config that was sent
        config = GenerationConfiguration.GetRootAs(req.configuration, 0)
        metadata_batch = _get_batch_metadata(config, req.prompt, req.negative_prompt)

        update, finish = self._updater(config, req, on_progress)

        generated_images: list[bytes] = []
        generated_audio = bytearray()

        try:
            async for response in self._service.generate_image(req):
                current_signpost = response.current_signpost
                preview = response.preview_image

                update(current_signpost, preview)

                if response.generated_images:
                    generated_images.extend(response.generated_images)

                if response.generated_audio:
                    generated_audio.extend(b"".join(response.generated_audio))

        except GRPCError as e:
            finish(0, True)
            raise_grpc_error(e)
        except Exception as e:
            finish(0, True)
            print(f"Error processing response: {e}")
            raise e

        finish(len(generated_images))

        if len(generated_images) == 0:
            raise RuntimeError("No images received from server")

        result: list[ImageBuffer] = []
        is_video = False

        if len(generated_images) != len(metadata_batch):
            # we can assume this is a video. batch size is ignored for video models
            # there is an edge case where the ignored batch_size equals number of frames
            # figure that out later
            is_video = True

        for i, image in enumerate(generated_images):
            image_metadata = metadata_batch[0] if is_video else metadata_batch[i]
            result.append(ImageBuffer.from_tensor(image, metadata=image_metadata))

        audio: AudioBuffer | None = None
        if generated_audio:
            audio = AudioBuffer.from_tensor(bytes(generated_audio))
            sample_rate = get_sample_rate(len(audio.data), len(result), 25)
            audio.sample_rate = sample_rate

        return ImageGenerationResult(images=result, audio=audio)

    def _print_start(self, req: image_service.ImageGenerationRequest):
        """Print a concise summary of what will be sent to the server.

        The helper inspects the request for an init image, hints, and
        mask information and prints a human-friendly message.
        """
        base = "Sending generation request"
        items: list[str] = []
        if req.image is not None:
            items.append("init image")
        if len(req.hints):
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

    def _updater(
        self,
        config: GenerationConfiguration,
        req: image_service.ImageGenerationRequest,
        on_progress: ProgressCallback | None,
    ):
        if not self._disable_messages:
            self._print_start(req)

        progressbar = None
        if self._progressbar:
            est_steps = _estimate_signposts(config, req)
            completed_steps = 0
            progressbar = tqdm.tqdm(desc="Generating", total=est_steps, ncols=80)

        def update(
            signpost: image_service.ImageGenerationSignpostProto | None,
            preview: bytes | None = None,
        ):
            nonlocal progressbar, on_progress, est_steps, completed_steps

            if signpost is None and preview is None:
                return

            if signpost is not None and progressbar is not None:
                signpost_text = format_signpost(signpost)
                completed_steps += 1
                if completed_steps <= est_steps:
                    _ = progressbar.update(1)
                progressbar.set_postfix_str(signpost_text)

            if on_progress is not None:
                preview_image = decode_preview(preview) if preview is not None else None
                on_progress(signpost, preview_image)

        def finish(count: int, failed: bool = False):
            nonlocal progressbar, est_steps, completed_steps

            if progressbar is not None:
                if failed:
                    progressbar.set_postfix_str("Request failed")
                else:
                    progressbar.set_postfix_str("Finished")
                    if completed_steps < est_steps:
                        _ = progressbar.update(est_steps - completed_steps)
                progressbar.close()

            if not self._disable_messages:
                print(f"Received {count} image{pluralize(count)}!")

        return update, finish


def _get_batch_metadata(
    config: GenerationConfiguration, prompt: str, negative_prompt: str
) -> list[ImageMetadata]:
    seeds = seeds_from_batch(
        config.Seed(),
        config.BatchSize(),
        cast(int, config.SeedMode()),  # pyright: ignore[reportUnknownMemberType]
    )
    metadata = create_metadata(
        config,
        prompt,
        negative_prompt,
    )
    metadata_batch = [copy_with_seed(metadata, seed) for seed in seeds]
    return metadata_batch


def _estimate_signposts(
    config: GenerationConfiguration, request: image_service.ImageGenerationRequest
) -> int:
    """Get an estimate of the total number of signposts that will be received. Used to estimate progress"""
    # TextEncoded, ImageEncoded, Sampling
    est = 3

    # +1 for each sent image
    est += 1 if request.image else 0
    est += sum([len(h.tensors) for h in request.hints])

    # +1 for each step * strength (here's where things get iffy)
    est += math.ceil(config.Steps() * config.Strength())

    # +3, +1 for each step in hires pass....
    est += (
        math.ceil(config.Steps() * config.HiresFixStrength() + 3)
        if config.HiresFix()
        else 0
    )

    # +2 for upscaling
    est += 2 if config.Upscaler() else 0

    # +1 for ImageDecoded
    est += 1

    return est


# def _get_service_stub(host: str, port: int) -> image_service.ImageGenerationServiceStub:
#     pass
