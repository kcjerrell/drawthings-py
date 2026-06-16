from abc import ABC, abstractmethod

from typing_extensions import override

from drawthings_py.generated.dt_grpc import image_service
from drawthings_py.models.types import ModelsInfo


class ModelsSource(ABC):  # noqa: F821
    _models: ModelsInfo
    _files: list[str]

    def __init__(self):
        self._models = ModelsInfo()
        self._files = []

    @abstractmethod
    async def load(self) -> None:
        pass

    pass


class GrpcModelsSource(ModelsSource):
    _service: image_service.ImageGenerationServiceStub

    def __init__(self, service: image_service.ImageGenerationServiceStub):
        super().__init__()
        self._service = service

    @override
    async def load(self) -> None:
        req = image_service.EchoRequest(
            "drawthings-py",
        )
        reply = await self._service.echo(req)

        models = reply.override.models if reply.override is not None else None
        print(f"{len(reply.files)} files. {len(models) if models else 0} models")

        if reply.override is None:
            return

        self._models: ModelsInfo = ModelsInfo.from_echo_reply(reply)
        self._files: list[str] = reply.files
        return
