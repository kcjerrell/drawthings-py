from drawthings_py import ImageBuffer, RequestBuilder
from drawthings_py.configs import GenConfig
from drawthings_py.request_builder import build_grpc_message


def build(req: RequestBuilder):
    (message, _) = build_grpc_message(req)
    return message


def test_create():
    req = RequestBuilder({"width": 999}, "hello", "goodbye")

    assert req.config.width == 999
    assert req._prompt == "hello"
    assert req._negative_prompt == "goodbye"

    message = build(req)

    assert message.prompt == "hello"
    assert message.negative_prompt == "goodbye"

    # width will be rounded to nearest 64
    assert GenConfig.from_fbs(message.configuration)["width"] == 1024


def test_add_remove_images():
    req = RequestBuilder({"width": 1024}, "hello", "goodbye")

    image = ImageBuffer(bytes([1]), 1, 1, 1)

    req.init_image(image)

    message = build(req)

    assert message.image is not None

    req.add_moodboard_image(image)
    req.add_moodboard_image(image)
    req.control_image(image, "pose")

    message = build(req)

    assert message.image is not None
    assert len(message.hints) == 2
    hint_images = sorted(map(lambda x: len(x.tensors), message.hints))
    assert hint_images == [1, 2]

    req.clear_moodboard()
    req.clear_init_image()

    message = build(req)

    assert message.image is None
    assert len(message.hints) == 1
