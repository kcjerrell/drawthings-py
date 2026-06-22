import json
from typing import Any, Required, TypeAlias, TypedDict, Literal, cast

from drawthings_py.generated.dt_grpc import image_service
from drawthings_py.util.mixins import ReprMixin


ModelVersion = Literal[
    "auraflow",
    "cosmos2.5_2b",
    "ernie_image",
    "flux1",
    "flux2",
    "flux2_4b",
    "flux2_9b",
    "hiDreamO1",
    "hidream_i1",
    "hunyuan_video",
    "ideogram4",
    "kandinsky2.1",
    "ltx2",
    "ltx2.3",
    "pixart",
    "qwen_image",
    "sd3",
    "sd3_large",
    "sdxl_base_v0.9",
    "sdxl_refiner_v0.9",
    "seedvr2_3b",
    "seedvr2_7b",
    "ssd_1b",
    "svd_i2v",
    "v1",
    "v2",
    "wan_v2.1_1.3b",
    "wan_v2.1_14b",
    "wan_v2.2_5b",
    "wurstchen_v3.0_stage_c",
    "z_image",
]

Modifier = Literal[
    "canny",
    "color",
    "depth",
    "double",
    "editing",
    "inpaint",
    "inpainting",
    "ip2p",
    "kontext",
    "kontext_kv",
    "lineart",
    "mlsd",
    "none",
    "normalbae",
    "pose",
    "qwenimageEdit2511",
    "qwenimageEditPlus",
    "qwenimageLayered",
    "qwenimage_edit_plus",
    "scribble",
    "seg",
    "shuffle",
    "softedge",
    "tile",
]


class ModelBase(TypedDict, total=False):
    """
    Common metadata for all model types

    Required fields:
    - name: The model's display name
    - file: The model's file name
    - version: Model architecture (SD 1.x, SDXL, Flux.1, etc.)

    Optional fields:
    - prefix: Text to be automatically prepended to the prompt field when using this model in the Draw Things app
    - modifier: Controls specialized processing behaviors (such as inpainting, editing, or reference image conditioning)
    - note: Additional information about this model
    - copyright: The model's copyright info
    """

    name: Required[str]
    """The model's display name"""
    file: Required[str]
    """The model's file name"""
    version: Required[ModelVersion]
    """Model architecture (SD 1.x, SDXL, Flux.1, etc.)."""
    prefix: str
    """Text to be automatically prepended to the prompt field when using this model in the Draw Things app"""
    modifier: Modifier
    """Controls specialized processing behaviors (such as inpainting, editing, or reference image conditioning)"""
    note: str
    """Additional information about this model"""
    copyright: str
    """The model's copyright info"""
    deprecated: bool
    """Whether this model is deprecated"""


class ImageModel(ModelBase, total=False):
    autoencoder: str
    clip_encoder: Literal["clip_l", "clip_g", "clip_l14"]
    text_encoder: Literal["clip_l", "clip_g", "clip_l14", "t5"]
    default_scale: float
    upcast_attention: bool
    high_precision_autoencoder: bool
    hires_fix_scale: float
    noise_discretization: Literal["EDM", "v_prediction", "epsilon"]
    objective: Literal["cfg", "cfg_rescale"]
    guidance_embed: bool
    mmdit: int
    is_consistency_model: bool
    image_encoder: str
    builtin_lora: list[str]


class ControlNetModel(ModelBase, total=False):
    autoencoder: str
    type: str
    preprocessor: str
    global_average_pooling: bool
    transformer_blocks: int
    image_encoder: str
    ip_adapter_config: dict[str, object]


class LoraModel(ModelBase, total=False):
    weight: float
    is_consistency_model: bool
    is_lo_ha: bool


class TextualInversionModel(ModelBase, total=False):
    keyword: str
    length: int


class UpscalerModel(TypedDict, total=False):
    name: Required[str]
    file: Required[str]
    blocks: int
    scale_factor: int


_jl: TypeAlias = list[dict[str, object]]


def _cjl(data: Any) -> _jl:  # pyright: ignore[reportExplicitAny, reportAny]
    return cast(_jl, data)


class ModelsInfo(ReprMixin):
    models: list[ImageModel]
    controlNets: list[ControlNetModel]
    loras: list[LoraModel]
    upscalers: list[UpscalerModel]
    textualInversions: list[TextualInversionModel]
    files: list[str]

    def __init__(
        self,
        models: list[ImageModel] | None = None,
        controlNets: list[ControlNetModel] | None = None,
        loras: list[LoraModel] | None = None,
        upscalers: list[UpscalerModel] | None = None,
        textualInversions: list[TextualInversionModel] | None = None,
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

        def has_req(item: dict[str, object]) -> bool:
            return "name" in item and "file" in item and "version" in item

        def has_req_u(item: dict[str, object]) -> bool:
            return "name" in item and "file" in item

        models = (
            [item for item in _cjl(json.loads(data.models)) if has_req(item)]
            if data.models
            else []
        )
        control_nets = (
            [item for item in _cjl(json.loads(data.control_nets)) if has_req(item)]
            if data.control_nets
            else []
        )
        loras = (
            [item for item in _cjl(json.loads(data.loras)) if has_req(item)]
            if data.loras
            else []
        )
        upscalers = (
            [item for item in _cjl(json.loads(data.upscalers)) if has_req_u(item)]
            if data.upscalers
            else []
        )
        textual_inversions = (
            [
                item
                for item in _cjl(json.loads(data.textual_inversions))
                if has_req(item)
            ]
            if data.textual_inversions
            else []
        )
        return cls(
            models=cast(list[ImageModel], models),
            controlNets=cast(list[ControlNetModel], control_nets),
            loras=cast(list[LoraModel], loras),
            upscalers=cast(list[UpscalerModel], upscalers),
            textualInversions=cast(list[TextualInversionModel], textual_inversions),
            files=files,
        )
