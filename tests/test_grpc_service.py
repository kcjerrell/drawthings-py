import asyncio

from drawthings_py import RequestBuilder
from drawthings_py.generated.dt_grpc import image_service
from drawthings_py.grpc_service import GrpcService, format_signpost
from drawthings_py.request_builder import _build_message

from grpc_service_mocks import MockImageGenerationServiceStub


def test_mock_image_generation_service_stub_streams_expected_responses(monkeypatch):
    monkeypatch.setattr("drawthings_py.request_builder.os.getlogin", lambda: "tester")

    request, _ = _build_message(
        RequestBuilder(
            {
                "width": 128,
                "height": 192,
                "steps": 3,
                "batch_size": 2,
            },
        ),
    )
    stub = MockImageGenerationServiceStub(channel=object())

    async def collect():
        return [response async for response in stub.generate_image(request)]

    responses = asyncio.run(collect())

    assert [
        format_signpost(response.current_signpost) for response in responses[:-1]
    ] == [
        "Text encoded",
        "Image encoded",
        "Sampling: step 0",
        "Sampling: step 1",
        "Sampling: step 2",
        "Sampling: step 3",
        "Image decoded",
    ]
    assert responses[-1].current_signpost is None
    assert len(responses[-1].generated_images) == 2

    preview_steps = [
        response.current_signpost.sampling.step
        for response in responses
        if response.current_signpost is not None
        and response.current_signpost.is_set("sampling")
        and response.preview_image is not None
    ]
    assert preview_steps == [0, 2]


def test_grpc_service_generate_image_uses_mock_stub(monkeypatch):
    monkeypatch.setattr(
        "drawthings_py.grpc_service.image_service.ImageGenerationServiceStub",
        MockImageGenerationServiceStub,
    )
    monkeypatch.setattr("drawthings_py.request_builder.os.getlogin", lambda: "tester")

    progress = []
    request = RequestBuilder(
        {
            "width": 128,
            "height": 192,
            "steps": 2,
            "batch_size": 2,
            "seed": 123,
        },
        prompt="black square",
    )
    request.on_progress(lambda signpost, preview: progress.append((signpost, preview)))

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    service = GrpcService(progressbar=False, disable_messages=True)
    try:
        images = asyncio.run(service.generate_image(request))
    finally:
        service._dispose()
        loop.close()

    assert len(images) == 2
    assert [(image.width, image.height, image.channels) for image in images] == [
        (128, 192, 3),
        (128, 192, 3),
    ]
    assert all(image.data == bytes(128 * 192 * 3) for image in images)

    preview_images = [preview for _, preview in progress if preview is not None]
    assert [(preview.width, preview.height) for preview in preview_images] == [
        (64, 64),
        (64, 64),
    ]
    assert all(
        isinstance(signpost, image_service.ImageGenerationSignpostProto)
        for signpost, _ in progress
        if signpost is not None
    )
