"""
Primary entry point for using Draw Things services
"""

from drawthings_py._dt_service import DrawThingsService


def cli(exec_path: str, temp_dir: str = "") -> DrawThingsService:
    """Create a Draw Things CLI service instance.

    Args:
        exec_path: Path to the Draw Things CLI executable.
        temp_dir: Directory for storing temporary files. Defaults to "".

    Returns:
        DrawThingsService: A CLI service instance.
    """
    from .cli_service import CliService  # pylint: disable=import-outside-toplevel

    return CliService(exec_path=exec_path, temp_dir=temp_dir)


def grpc(
    host: str = "127.0.0.1",
    port: int = 7859,
    progressbar: bool = True,
    disable_messages: bool = False,
) -> DrawThingsService:
    """Connect to a Draw Things gRPC server.

    Args:
        host: The host of the gRPC server. Defaults to "127.0.0.1".
        port: The port of the gRPC server. Defaults to 7859.
        progressbar: Whether to display a progress bar during image generation. Defaults to True.
        disable_messages: Whether to disable gRPC log messages. Defaults to False.

    Returns:
        DrawThingsService: A gRPC service instance connected to the specified server.
    """
    from .grpc.grpc_service import GrpcService  # pylint: disable=import-outside-toplevel

    return GrpcService(
        host=host, port=port, progressbar=progressbar, disable_messages=disable_messages
    )
