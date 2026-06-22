from typing_extensions import override

from drawthings_py.image_generation_result import ImageGenerationResult
from drawthings_py.models.types import ModelsInfo

from ._dt_service import DrawThingsService
from .request_builder import RequestBuilder


class CliService(DrawThingsService):
    """
    not yet implemented
    """

    def __init__(self, exec_path: str, temp_dir: str = ""):
        """
        Not yet implemented
        """
        super().__init__()
        raise NotImplementedError("this is not implemented yet")

    @override
    async def get_models(self, refresh_cache: bool = False) -> ModelsInfo:
        """
        Not yet implemented
        """
        raise NotImplementedError("this is not implemented yet")

    @override
    async def generate_image(self, request: RequestBuilder) -> ImageGenerationResult:
        """
        Not yet implemented
        """
        raise NotImplementedError("this is not implemented yet")

    @override
    async def connect(self) -> None:
        """
        Not yet implemented
        """
        raise NotImplementedError("this is not implemented yet")

    @override
    async def close(self) -> None:
        """
        Not yet implemented
        """
        raise NotImplementedError("this is not implemented yet")
