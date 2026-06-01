"""
Primary entry point for using Draw Things services
"""

from __future__ import annotations

from drawthings_py._dt_service import DrawThingsService


def cli(exec_path: str, temp_dir: str = "") -> DrawThingsService:
    """
    Not yet implemented
    """
    from .cli_service import CliService  # pylint: disable=import-outside-toplevel

    return CliService(exec_path=exec_path, temp_dir=temp_dir)


def grpc(host: str = "127.0.0.1", port: int = 7859) -> DrawThingsService:
    """
    Connect to a Draw Things gRPC server

    host: str - the host of the gRPC server
    port: int - the port of the gRPC server
    return: GrpcService - the gRPC service
    """
    from .grpc_service import GrpcService  # pylint: disable=import-outside-toplevel

    return GrpcService(host=host, port=port)
