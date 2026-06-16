import json
from typing import Any, Literal, TypeAlias, cast

from drawthings_py.generated.dt_grpc import image_service
from drawthings_py.util.mixins import ReprMixin

ModelTypes = Literal[
    "models", "controlnets", "loras", "upscalers", "textual_inversions"
]


class ModelBase(ReprMixin):
    file: str = ""
    name: str = ""

    def __init__(self, **kwargs: object):
        for key, value in kwargs.items():
            setattr(self, key, value)


class ModelInfo(ModelBase):
    prefix: str = ""
    version: str = ""


class ControlNetInfo(ModelBase):
    modifier: str = ""
    type: str = ""
    global_average_pooling: bool = False
    version: str = ""


class LoRAInfo(ModelBase):
    prefix: str = ""
    mode: str = ""
    version: str = ""


class UpscalerInfo(ModelBase):
    pass


class TextualInversionInfo(ModelBase):
    keyword: str = ""


_jl: TypeAlias = list[dict[str, object]]


def _cjl(data: Any) -> _jl:  # pyright: ignore[reportExplicitAny, reportAny]
    return cast(_jl, data)


class ModelsInfo(ReprMixin):
    models: list[ModelInfo]
    controlNets: list[ControlNetInfo]
    loras: list[LoRAInfo]
    upscalers: list[UpscalerInfo]
    textualInversions: list[TextualInversionInfo]
    files: list[str]

    def __init__(
        self,
        models: list[ModelInfo] | None = None,
        controlNets: list[ControlNetInfo] | None = None,
        loras: list[LoRAInfo] | None = None,
        upscalers: list[UpscalerInfo] | None = None,
        textualInversions: list[TextualInversionInfo] | None = None,
        files: list[str] | None = None,
    ):
        self.models = models or []
        self.controlNets = controlNets or []
        self.loras = loras or []
        self.upscalers = upscalers or []
        self.textualInversions = textualInversions or []
        self.files = files or []

    @classmethod
    def from_echo_reply(cls, reply: image_service.EchoReply) -> "ModelsInfo":
        data = reply.override
        files = reply.files or []

        if data is None:
            return cls(files=files)

        models = (
            [ModelInfo(**item) for item in _cjl(json.loads(data.models))]
            if data.models
            else []
        )
        control_nets = (
            [ControlNetInfo(**item) for item in _cjl(json.loads(data.control_nets))]
            if data.control_nets
            else []
        )
        loras = (
            [LoRAInfo(**item) for item in _cjl(json.loads(data.loras))]
            if data.loras
            else []
        )
        upscalers = (
            [UpscalerInfo(**item) for item in _cjl(json.loads(data.upscalers))]
            if data.upscalers
            else []
        )
        textual_inversions = (
            [
                TextualInversionInfo(**item)
                for item in _cjl(json.loads(data.textual_inversions))
            ]
            if data.textual_inversions
            else []
        )
        return cls(
            models=models,
            controlNets=control_nets,
            loras=loras,
            upscalers=upscalers,
            textualInversions=textual_inversions,
            files=reply.files,
        )
