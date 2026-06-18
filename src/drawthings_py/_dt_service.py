"""
Primary entry point for using Draw Things services
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from types import TracebackType

from drawthings_py.image_generation_result import ImageGenerationResult
from drawthings_py.models.types import ModelsInfo

from .request_builder import RequestBuilder


class DrawThingsService(ABC):
    """
    Base class for grpc and cii service
    """

    @abstractmethod
    async def generate_image(self, request: RequestBuilder) -> ImageGenerationResult:
        """
        Generate an image from the provided request builder
        """

    @abstractmethod
    async def get_models(self) -> ModelsInfo:
        """
        Get models from the service
        """

    @abstractmethod
    def _dispose(self):
        """
        dispose of the service
        """

    async def __aenter__(self) -> "DrawThingsService":
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self._dispose()
