"""
Primary entry point for using Draw Things services
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from .request_builder import RequestBuilder
from .image_buffer import ImageBuffer


class DrawThingsService(ABC):
    """
    Base class for grpc and cii service
    """

    @abstractmethod
    async def generate_image(self, request: RequestBuilder) -> list[ImageBuffer]:
        """
        Generate an image from the provided request builder
        """

    @abstractmethod
    def _dispose(self):
        """
        dispose of the service
        """

    async def __aenter__(self) -> "DrawThingsService":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._dispose()
