"""
primary entry point for using Draw Things services
"""

from abc import ABC, abstractmethod
import inspect
from .request_builder import RequestBuilder
from .image_buffer import ImageBuffer


class DrawThingsService(ABC):
    """
    Provides access to image generation with Draw Things
    """

    @abstractmethod
    async def generate_image(self, request: RequestBuilder) -> list[ImageBuffer]:
        """
        generate an image from the provided request builder
        """
        pass

    @abstractmethod
    async def _dispose(self):
        """
        dispose of the service
        """

    @classmethod
    def cli(cls, exec_path: str, temp_dir: str = "") -> DrawThingsService:  # type: ignore
        """
        not yet implemented
        """
        from .cli_service import CliService

        return CliService(exec_path=exec_path, temp_dir=temp_dir)

    @classmethod
    def grpc(cls, host: str = "127.0.0.1", port: int = 7859) -> DrawThingsService:  # type: ignore
        """
        connect to a Draw Things gRPC server

        host: str - the host of the gRPC server
        port: int - the port of the gRPC server
        return: GrpcService - the gRPC service
        """
        from .grpc_service import GrpcService

        return GrpcService(host=host, port=port)

    async def __aenter__(self) -> "DrawThingsService":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self, "_dispose"):
            result = self._dispose()
            if inspect.isawaitable(result):
                await result
