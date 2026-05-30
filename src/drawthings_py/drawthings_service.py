"""
Primary entry point for using Draw Things services
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from .request_builder import RequestBuilder
from .image_buffer import ImageBuffer


class DrawThingsService(ABC):
    """
    Provides access to image generation with Draw Things
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

    @classmethod
    def cli(cls, exec_path: str, temp_dir: str = "") -> DrawThingsService:
        """
        Not yet implemented
        """
        from .cli_service import CliService  # pylint: disable=import-outside-toplevel

        return CliService(exec_path=exec_path, temp_dir=temp_dir)

    @classmethod
    def grpc(cls, host: str = "127.0.0.1", port: int = 7859) -> DrawThingsService:
        """
        Connect to a Draw Things gRPC server

        host: str - the host of the gRPC server
        port: int - the port of the gRPC server
        return: GrpcService - the gRPC service
        """
        from .grpc_service import GrpcService  # pylint: disable=import-outside-toplevel

        return GrpcService(host=host, port=port)

    async def __aenter__(self) -> "DrawThingsService":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._dispose()
