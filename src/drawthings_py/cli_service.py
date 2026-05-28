from .drawthings_service import DrawThingsService
from .request_builder import RequestBuilder
from .image_buffer import ImageBuffer


class CliService(DrawThingsService):
    """
    not yet implemented
    """
    def __init__(self, exec_path: str, temp_dir: str = ""):
        raise NotImplementedError("this is not implemented yet")

    async def generate_image(self, request: RequestBuilder) -> list[ImageBuffer]:
        raise NotImplementedError("this is not implemented yet")

    def _dispose(self):
        raise NotImplementedError("this is not implemented yet")
