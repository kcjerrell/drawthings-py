from abc import ABC, abstractmethod
import inspect
from .request_builder import RequestBuilder
from .image_buffer import ImageBuffer


class DrawThingsService(ABC):
    """
    abstract base class. see CliService or GrpcService to use
    """

    @abstractmethod
    async def generate_image(self, request: RequestBuilder) -> list[ImageBuffer]:
        """
        generate an image from the provided request builder
        """
        pass

    @classmethod
    def cli(cls, exec_path: str, temp_dir: str = "") -> "CliService":
        """
        not yet implemented
        """
        from .cli_service import CliService

        return CliService(exec_path=exec_path, temp_dir=temp_dir)

    @classmethod
    def grpc(cls, host: str = "127.0.0.1", port: int = 7859) -> "GrpcService":
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
        if hasattr(self, "dispose"):
            result = self.dispose()
            if inspect.isawaitable(result):
                await result
