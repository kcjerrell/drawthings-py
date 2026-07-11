from __future__ import annotations

from collections.abc import AsyncIterator

from drawthings_py.generated.dt_grpc.config_generated import (
    GenerationConfiguration,
)
from drawthings_py.generated.dt_grpc import image_service
from drawthings_py.image.image_buffer import ImageBuffer


def black_image_tensor(width: int, height: int, channels: int = 3) -> bytes:
    """Build a black image tensor using the production ImageBuffer conversion."""
    return ImageBuffer(
        data=bytes(width * height * channels),
        width=width,
        height=height,
        channels=channels,  # type: ignore  # pyright: ignore[reportArgumentType]
    ).to_tensor()


class MockImageGenerationServiceStub:
    """Fake image generation stub for grpc_service tests."""

    requests: list[image_service.ImageGenerationRequest]

    def __init__(self, channel):
        self.channel = channel
        self.requests = []

    async def echo(self, _: image_service.EchoRequest) -> image_service.EchoReply:
        return image_service.EchoReply(message="drawthings-py")

    async def generate_image(
        self,
        generation_request: image_service.ImageGenerationRequest,
    ) -> AsyncIterator[image_service.ImageGenerationResponse]:
        self.requests.append(generation_request)

        config = GenerationConfiguration.GetRootAs(generation_request.configuration, 0)
        steps = config.Steps()
        width = config.StartWidth() * 64
        height = config.StartHeight() * 64
        batch_size = config.BatchSize()

        yield image_service.ImageGenerationResponse(
            current_signpost=image_service.ImageGenerationSignpostProto(
                text_encoded=image_service.ImageGenerationSignpostProtoTextEncoded(),
            ),
        )
        yield image_service.ImageGenerationResponse(
            current_signpost=image_service.ImageGenerationSignpostProto(
                image_encoded=image_service.ImageGenerationSignpostProtoImageEncoded(),
            ),
        )

        preview = black_image_tensor(64, 64)
        for step in range(steps + 1):
            yield image_service.ImageGenerationResponse(
                current_signpost=image_service.ImageGenerationSignpostProto(
                    sampling=image_service.ImageGenerationSignpostProtoSampling(
                        step=step,
                    ),
                ),
                preview_image=preview if step % 2 == 0 else None,
            )

        yield image_service.ImageGenerationResponse(
            current_signpost=image_service.ImageGenerationSignpostProto(
                image_decoded=image_service.ImageGenerationSignpostProtoImageDecoded(),
            ),
        )
        yield image_service.ImageGenerationResponse(
            generated_images=[
                black_image_tensor(width, height) for _ in range(batch_size)
            ],
        )
