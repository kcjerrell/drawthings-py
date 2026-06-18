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
        raise NotImplementedError("this is not implemented yet")

    @override
    async def get_models(self) -> ModelsInfo:
        raise NotImplementedError("this is not implemented yet")

    @override
    async def generate_image(self, request: RequestBuilder) -> ImageGenerationResult:
        raise NotImplementedError("this is not implemented yet")

    @override
    def _dispose(self) -> None:
        raise NotImplementedError("this is not implemented yet")
