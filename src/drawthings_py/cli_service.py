from typing_extensions import override

from ._dt_service import DrawThingsService
from .request_builder import RequestBuilder
from .image_buffer import ImageBuffer


class CliService(DrawThingsService):
    """
    not yet implemented
    """

    def __init__(self, exec_path: str, temp_dir: str = ""):
        """
        Not yet implemented
        """
        raise NotImplementedError("this is not implemented yet")

    @override
    async def generate_image(self, request: RequestBuilder) -> list[ImageBuffer]:
        raise NotImplementedError("this is not implemented yet")

    @override
    def _dispose(self) -> None:
        raise NotImplementedError("this is not implemented yet")
