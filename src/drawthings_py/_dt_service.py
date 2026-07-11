"""
Base class for Draw Things service
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from types import TracebackType

from drawthings_py.image_generation_result import ImageGenerationResult
from drawthings_py.models.types import ModelsInfo

from .request_builder import RequestBuilder


class DrawThingsService(ABC):
    """
    Provides access to Draw Things's image generation.
    """

    _aenter_depth: int

    def __init__(self):
        self._aenter_depth = 0

    @abstractmethod
    async def generate(self, request: RequestBuilder) -> ImageGenerationResult:
        """
        Send a generation request and collect generated images.

        Progress updates and preview images can be received by attaching a callback
        to the RequestBuilder.

        Returns:
            An ImageGenerationResult, containing the generated image(s) and audio, if any.
        """

    async def generate_image(self, request: RequestBuilder) -> ImageGenerationResult:
        """
        Deprecated alias to generate().

        This method is deprecated and will be removed in a future release.
        Use generate() instead.
        """
        import warnings

        warnings.warn(
            "generate_image is a deprecated alias to generate(), use generate() instead.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        return await self.generate(request)

    @abstractmethod
    async def get_models(self, refresh_cache: bool = False) -> ModelsInfo:
        """
        Get the (cached) list of models and files from the service
        args:
            refresh_cache: Whether to refresh the cache
        """

    @abstractmethod
    async def connect(self):
        """
        Ensures that the service is ready to use
        This will be called automatically when using the service as a context manager,
        ('async with...'), or when calling any other methods that require the service to be connected.
        """
        ...

    @abstractmethod
    async def close(self):
        """
        Disposes of the service, closing any connections and removing any temporary files
        This will be called automatically when using the service as a context manager ('async with...')
        """

    async def __aenter__(self) -> "DrawThingsService":
        """
        Async context manager entry.
        """
        self._aenter_depth += 1
        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        Async context manager exit.
        """
        self._aenter_depth -= 1
        if self._aenter_depth == 0:
            await self.close()
