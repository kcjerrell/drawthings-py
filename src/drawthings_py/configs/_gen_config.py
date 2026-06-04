from .types import ConfigDict
from drawthings_py.generated.dt_grpc.config_generated import GenerationConfiguration


def build_config(config: ConfigDict, seed: int | None = None) -> bytes:
    return b""
