from collections.abc import MutableMapping, Iterator
from typing import Unpack, overload, Literal, TypedDict, cast
from typing_extensions import override
from drawthings_py.configs.types import (
    LoraDict,
    UpscalerModel,
    CompressionMethod,
    SamplerType,
    SeedMode,
)


GenConfigKey = Literal[
    "id",
    "width",
    "height",
    "seed",
    "steps",
    "guidance",
    "strength",
    "model",
    "sampler",
    "loras",
    "batch_count",
    "batch_size",
    "hires_fix",
    "hires_fix_width",
    "hires_fix_height",
    "hires_fix_strength",
    "upscaler",
    "image_guidance_scale",
    "seed_mode",
    "clip_skip",
    "mask_blur",
    "face_restoration",
    "decode_with_attention",
    "hires_fix_decode_with_attention",
    "clip_weight",
    "negative_prompt_for_image_prior",
    "image_prior_steps",
    "refiner_model",
    "original_image_height",
    "original_image_width",
    "crop_top",
    "crop_left",
    "target_image_height",
    "target_image_width",
    "aesthetic_score",
    "negative_aesthetic_score",
    "zero_negative_prompt",
    "refiner_start",
    "negative_original_image_height",
    "negative_original_image_width",
    "name",
    "fps",
    "motion_scale",
    "guiding_frame_noise",
    "guiding_frame_guidance",
    "num_frames",
    "mask_blur_outset",
    "sharpness",
    "shift",
    "stage_2_steps",
    "stage_2_cfg",
    "stage_2_shift",
    "tiled_decoding",
    "decoding_tile_width",
    "decoding_tile_height",
    "decoding_tile_overlap",
    "stochastic_sampling_gamma",
    "preserve_original_after_inpaint",
    "tiled_diffusion",
    "diffusion_tile_width",
    "diffusion_tile_height",
    "diffusion_tile_overlap",
    "upscaler_scale_factor",
    "t5_text_encoder",
    "separate_clip_l",
    "clip_l_text",
    "separate_open_clip_g",
    "open_clip_g_text",
    "speed_up_with_guidance_embed",
    "guidance_embed",
    "resolution_dependent_shift",
    "tea_cache_start",
    "tea_cache_end",
    "tea_cache_threshold",
    "tea_cache",
    "separate_t5",
    "t5_text",
    "tea_cache_max_skip_steps",
    "causal_inference_enabled",
    "causal_inference",
    "causal_inference_pad",
    "cfg_zero_star",
    "cfg_zero_init_steps",
    "compression_artifacts",
    "compression_artifacts_quality",
]

GenConfigIntKey = Literal[
    "id",
    "width",
    "height",
    "seed",
    "steps",
    "batch_count",
    "batch_size",
    "hires_fix_width",
    "hires_fix_height",
    "clip_skip",
    "image_prior_steps",
    "original_image_height",
    "original_image_width",
    "crop_top",
    "crop_left",
    "target_image_height",
    "target_image_width",
    "negative_original_image_height",
    "negative_original_image_width",
    "fps",
    "motion_scale",
    "num_frames",
    "mask_blur_outset",
    "stage_2_steps",
    "decoding_tile_width",
    "decoding_tile_height",
    "decoding_tile_overlap",
    "diffusion_tile_width",
    "diffusion_tile_height",
    "diffusion_tile_overlap",
    "upscaler_scale_factor",
    "tea_cache_start",
    "tea_cache_end",
    "tea_cache_max_skip_steps",
    "causal_inference",
    "causal_inference_pad",
    "cfg_zero_init_steps",
]
GenConfigFloatKey = Literal[
    "guidance",
    "strength",
    "hires_fix_strength",
    "image_guidance_scale",
    "mask_blur",
    "clip_weight",
    "aesthetic_score",
    "negative_aesthetic_score",
    "refiner_start",
    "guiding_frame_noise",
    "guiding_frame_guidance",
    "sharpness",
    "shift",
    "stage_2_cfg",
    "stage_2_shift",
    "stochastic_sampling_gamma",
    "guidance_embed",
    "tea_cache_threshold",
    "compression_artifacts_quality",
]
GenConfigStrKey = Literal[
    "model",
    "face_restoration",
    "refiner_model",
    "name",
    "clip_l_text",
    "open_clip_g_text",
    "t5_text",
]
GenConfigBoolKey = Literal[
    "hires_fix",
    "decode_with_attention",
    "hires_fix_decode_with_attention",
    "negative_prompt_for_image_prior",
    "zero_negative_prompt",
    "tiled_decoding",
    "preserve_original_after_inpaint",
    "tiled_diffusion",
    "t5_text_encoder",
    "separate_clip_l",
    "separate_open_clip_g",
    "speed_up_with_guidance_embed",
    "resolution_dependent_shift",
    "tea_cache",
    "separate_t5",
    "causal_inference_enabled",
    "cfg_zero_star",
]
CoreConfigKey = Literal[
    "width",
    "height",
    "seed",
    "steps",
    "guidance",
    "strength",
    "model",
    "sampler",
    "loras",
    "shift",
    "resolution_dependent_shift",
]

CoreConfigIntKey = Literal[
    "width",
    "height",
    "seed",
    "steps",
]
ExtraConfigKey = Literal[
    "batch_size",
    "image_guidance_scale",
    "seed_mode",
    "clip_skip",
    "mask_blur",
    "face_restoration",
    "zero_negative_prompt",
    "num_frames",
    "mask_blur_outset",
    "sharpness",
    "stochastic_sampling_gamma",
    "preserve_original_after_inpaint",
]

ExtraConfigIntKey = Literal[
    "batch_size",
    "clip_skip",
    "num_frames",
    "mask_blur_outset",
]
ExtraConfigFloatKey = Literal[
    "image_guidance_scale",
    "mask_blur",
    "sharpness",
    "stochastic_sampling_gamma",
]
HiResFixConfigKey = Literal[
    "hires_fix",
    "hires_fix_width",
    "hires_fix_height",
    "hires_fix_strength",
]

UpscalerConfigKey = Literal[
    "upscaler",
    "upscaler_scale_factor",
]

RefinerConfigKey = Literal[
    "refiner_model",
    "refiner_start",
]

TiledConfigKey = Literal[
    "tiled_decoding",
    "decoding_tile_width",
    "decoding_tile_height",
    "decoding_tile_overlap",
    "tiled_diffusion",
    "diffusion_tile_width",
    "diffusion_tile_height",
    "diffusion_tile_overlap",
]

TiledConfigIntKey = Literal[
    "decoding_tile_width",
    "decoding_tile_height",
    "decoding_tile_overlap",
    "diffusion_tile_width",
    "diffusion_tile_height",
    "diffusion_tile_overlap",
]


class ConfigDict(TypedDict, total=False):
    id: int
    """"""
    width: int
    """how wide"""
    height: int
    """"""
    seed: int
    """"""
    steps: int
    """"""
    guidance: float
    """"""
    strength: float
    """"""
    model: str | None
    """the model"""
    sampler: SamplerType
    """"""
    loras: list[LoraDict]
    """"""
    batch_count: int
    """"""
    batch_size: int
    """"""
    hires_fix: bool
    """"""
    hires_fix_width: int
    """"""
    hires_fix_height: int
    """"""
    hires_fix_strength: float
    """"""
    upscaler: UpscalerModel | None
    """"""
    image_guidance_scale: float
    """"""
    seed_mode: SeedMode
    """"""
    clip_skip: int
    """"""
    mask_blur: float
    """"""
    face_restoration: str | None
    """"""
    decode_with_attention: bool
    """"""
    hires_fix_decode_with_attention: bool
    """"""
    clip_weight: float
    """"""
    negative_prompt_for_image_prior: bool
    """"""
    image_prior_steps: int
    """"""
    refiner_model: str | None
    """"""
    original_image_height: int
    """"""
    original_image_width: int
    """"""
    crop_top: int
    """"""
    crop_left: int
    """"""
    target_image_height: int
    """"""
    target_image_width: int
    """"""
    aesthetic_score: float
    """"""
    negative_aesthetic_score: float
    """"""
    zero_negative_prompt: bool
    """"""
    refiner_start: float
    """"""
    negative_original_image_height: int
    """"""
    negative_original_image_width: int
    """"""
    name: str | None
    """"""
    fps: int
    """"""
    motion_scale: int
    """"""
    guiding_frame_noise: float
    """"""
    guiding_frame_guidance: float
    """"""
    num_frames: int
    """"""
    mask_blur_outset: int
    """"""
    sharpness: float
    """"""
    shift: float
    """"""
    stage_2_steps: int
    """"""
    stage_2_cfg: float
    """"""
    stage_2_shift: float
    """"""
    tiled_decoding: bool
    """"""
    decoding_tile_width: int
    """"""
    decoding_tile_height: int
    """"""
    decoding_tile_overlap: int
    """"""
    stochastic_sampling_gamma: float
    """"""
    preserve_original_after_inpaint: bool
    """"""
    tiled_diffusion: bool
    """"""
    diffusion_tile_width: int
    """"""
    diffusion_tile_height: int
    """"""
    diffusion_tile_overlap: int
    """"""
    upscaler_scale_factor: int
    """"""
    t5_text_encoder: bool
    """"""
    separate_clip_l: bool
    """"""
    clip_l_text: str | None
    """"""
    separate_open_clip_g: bool
    """"""
    open_clip_g_text: str | None
    """"""
    speed_up_with_guidance_embed: bool
    """"""
    guidance_embed: float
    """"""
    resolution_dependent_shift: bool
    """"""
    tea_cache_start: int
    """"""
    tea_cache_end: int
    """"""
    tea_cache_threshold: float
    """"""
    tea_cache: bool
    """"""
    separate_t5: bool
    """"""
    t5_text: str | None
    """"""
    tea_cache_max_skip_steps: int
    """"""
    causal_inference_enabled: bool
    """"""
    causal_inference: int
    """"""
    causal_inference_pad: int
    """"""
    cfg_zero_star: bool
    """"""
    cfg_zero_init_steps: int
    """"""
    compression_artifacts: CompressionMethod
    """"""
    compression_artifacts_quality: float
    """"""


class GenConfig(MutableMapping[GenConfigKey, object]):
    _d: ConfigDict

    def __init__(self, **kwargs: Unpack[ConfigDict]):
        self._d = ConfigDict(**kwargs)

    @overload
    def __setitem__(self, key: GenConfigIntKey, value: int) -> None: ...
    @overload
    def __setitem__(self, key: GenConfigFloatKey, value: float) -> None: ...
    @overload
    def __setitem__(self, key: GenConfigStrKey, value: str | None) -> None: ...
    @overload
    def __setitem__(self, key: Literal["sampler"], value: SamplerType) -> None: ...
    @overload
    def __setitem__(self, key: Literal["loras"], value: list[LoraDict]) -> None: ...
    @overload
    def __setitem__(self, key: GenConfigBoolKey, value: bool) -> None: ...
    @overload
    def __setitem__(
        self, key: Literal["upscaler"], value: UpscalerModel | None
    ) -> None: ...
    @overload
    def __setitem__(self, key: Literal["seed_mode"], value: SeedMode) -> None: ...
    @overload
    def __setitem__(
        self, key: Literal["compression_artifacts"], value: CompressionMethod
    ) -> None: ...
    @override
    def __setitem__(self, key: GenConfigKey, value: object) -> None:
        self._d[key] = value

    @override
    def __delitem__(self, key: GenConfigKey) -> None:
        del self._d[key]

    @override
    def __iter__(self) -> Iterator[GenConfigKey]:
        return cast(Iterator[GenConfigKey], iter(self._d))

    @override
    def __len__(self) -> int:
        return len(self._d)

    @overload
    def __getitem__(self, key: GenConfigIntKey) -> int: ...
    @overload
    def __getitem__(self, key: GenConfigFloatKey) -> float: ...
    @overload
    def __getitem__(self, key: GenConfigStrKey) -> str | None: ...
    @overload
    def __getitem__(self, key: Literal["sampler"]) -> SamplerType: ...
    @overload
    def __getitem__(self, key: Literal["loras"]) -> list[LoraDict]: ...
    @overload
    def __getitem__(self, key: GenConfigBoolKey) -> bool: ...
    @overload
    def __getitem__(self, key: Literal["upscaler"]) -> UpscalerModel | None: ...
    @overload
    def __getitem__(self, key: Literal["seed_mode"]) -> SeedMode: ...
    @overload
    def __getitem__(
        self, key: Literal["compression_artifacts"]
    ) -> CompressionMethod: ...
    @override
    def __getitem__(self, key: GenConfigKey) -> object:
        return self._d[key]

    def __or__(self, other: "GenConfig") -> "GenConfig":
        combined = self._d | other._d
        return GenConfig(**combined)


class CoreConfig(GenConfig):
    def __init__(
        self,
        /,
        width: int | None = None,
        height: int | None = None,
        seed: int | None = -1,
        steps: int | None = None,
        guidance: float | None = 4.5,
        strength: float | None = None,
        model: str | None | None = None,
        sampler: SamplerType | None = SamplerType.DPMPP2MKarras,
        loras: list[LoraDict] | None = None,
        shift: float | None = 1.0,
        resolution_dependent_shift: bool | None = True,
    ):
        kwargs = {k: v for k, v in locals().items() if k != "self" and v is not None}

        super().__init__(**kwargs)

    @overload
    def __setitem__(self, key: CoreConfigIntKey, value: int) -> None: ...
    @overload
    def __setitem__(
        self, key: Literal["guidance", "strength", "shift"], value: float
    ) -> None: ...
    @overload
    def __setitem__(self, key: Literal["model"], value: str | None) -> None: ...
    @overload
    def __setitem__(self, key: Literal["sampler"], value: SamplerType) -> None: ...
    @overload
    def __setitem__(self, key: Literal["loras"], value: list[LoraDict]) -> None: ...
    @overload
    def __setitem__(
        self, key: Literal["resolution_dependent_shift"], value: bool
    ) -> None: ...
    @override
    def __setitem__(self, key: CoreConfigKey, value: object) -> None:
        self._d[key] = value

    @overload
    def __getitem__(self, key: CoreConfigIntKey) -> int: ...
    @overload
    def __getitem__(self, key: Literal["guidance", "strength", "shift"]) -> float: ...
    @overload
    def __getitem__(self, key: Literal["model"]) -> str | None: ...
    @overload
    def __getitem__(self, key: Literal["sampler"]) -> SamplerType: ...
    @overload
    def __getitem__(self, key: Literal["loras"]) -> list[LoraDict]: ...
    @overload
    def __getitem__(self, key: Literal["resolution_dependent_shift"]) -> bool: ...
    @override
    def __getitem__(self, key: CoreConfigKey) -> object:
        return self._d[key]


class ExtraConfig(GenConfig):
    def __init__(
        self,
        batch_size: int | None = 1,
        image_guidance_scale: float | None = 1.5,
        seed_mode: SeedMode | None = SeedMode.ScaleAlike,
        clip_skip: int | None = 1,
        mask_blur: float | None = None,
        face_restoration: str | None | None = None,
        zero_negative_prompt: bool | None = False,
        num_frames: int | None = 14,
        mask_blur_outset: int | None = 0,
        sharpness: float | None = 0,
        stochastic_sampling_gamma: float | None = 0.3,
        preserve_original_after_inpaint: bool | None = True,
    ):
        kwargs = {k: v for k, v in locals().items() if k != "self" and v is not None}

        super().__init__(**kwargs)

    @overload
    def __setitem__(self, key: ExtraConfigIntKey, value: int) -> None: ...
    @overload
    def __setitem__(self, key: ExtraConfigFloatKey, value: float) -> None: ...
    @overload
    def __setitem__(self, key: Literal["seed_mode"], value: SeedMode) -> None: ...
    @overload
    def __setitem__(
        self, key: Literal["face_restoration"], value: str | None
    ) -> None: ...
    @overload
    def __setitem__(
        self,
        key: Literal["zero_negative_prompt", "preserve_original_after_inpaint"],
        value: bool,
    ) -> None: ...
    @override
    def __setitem__(self, key: ExtraConfigKey, value: object) -> None:
        self._d[key] = value

    @overload
    def __getitem__(self, key: ExtraConfigIntKey) -> int: ...
    @overload
    def __getitem__(self, key: ExtraConfigFloatKey) -> float: ...
    @overload
    def __getitem__(self, key: Literal["seed_mode"]) -> SeedMode: ...
    @overload
    def __getitem__(self, key: Literal["face_restoration"]) -> str | None: ...
    @overload
    def __getitem__(
        self, key: Literal["zero_negative_prompt", "preserve_original_after_inpaint"]
    ) -> bool: ...
    @override
    def __getitem__(self, key: ExtraConfigKey) -> object:
        return self._d[key]


class HiResFixConfig(GenConfig):
    def __init__(
        self,
        hires_fix: bool | None = False,
        hires_fix_width: int | None = 512,
        hires_fix_height: int | None = 512,
        hires_fix_strength: float | None = 0.7,
    ):
        kwargs = {k: v for k, v in locals().items() if k != "self" and v is not None}

        super().__init__(**kwargs)

    @overload
    def __setitem__(self, key: Literal["hires_fix"], value: bool) -> None: ...
    @overload
    def __setitem__(
        self, key: Literal["hires_fix_width", "hires_fix_height"], value: int
    ) -> None: ...
    @overload
    def __setitem__(self, key: Literal["hires_fix_strength"], value: float) -> None: ...
    @override
    def __setitem__(self, key: HiResFixConfigKey, value: object) -> None:
        self._d[key] = value

    @overload
    def __getitem__(self, key: Literal["hires_fix"]) -> bool: ...
    @overload
    def __getitem__(
        self, key: Literal["hires_fix_width", "hires_fix_height"]
    ) -> int: ...
    @overload
    def __getitem__(self, key: Literal["hires_fix_strength"]) -> float: ...
    @override
    def __getitem__(self, key: HiResFixConfigKey) -> object:
        return self._d[key]


class UpscalerConfig(GenConfig):
    def __init__(
        self,
        upscaler: UpscalerModel | None | None = None,
        upscaler_scale_factor: int | None = 0,
    ):
        kwargs = {k: v for k, v in locals().items() if k != "self" and v is not None}

        super().__init__(**kwargs)

    @overload
    def __setitem__(
        self, key: Literal["upscaler"], value: UpscalerModel | None
    ) -> None: ...
    @overload
    def __setitem__(
        self, key: Literal["upscaler_scale_factor"], value: int
    ) -> None: ...
    @override
    def __setitem__(self, key: UpscalerConfigKey, value: object) -> None:
        self._d[key] = value

    @overload
    def __getitem__(self, key: Literal["upscaler"]) -> UpscalerModel | None: ...
    @overload
    def __getitem__(self, key: Literal["upscaler_scale_factor"]) -> int: ...
    @override
    def __getitem__(self, key: UpscalerConfigKey) -> object:
        return self._d[key]


class RefinerConfig(GenConfig):
    def __init__(
        self,
        refiner_model: str | None | None = None,
        refiner_start: float | None = 0.7,
    ):
        kwargs = {k: v for k, v in locals().items() if k != "self" and v is not None}

        super().__init__(**kwargs)

    @overload
    def __setitem__(self, key: Literal["refiner_model"], value: str | None) -> None: ...
    @overload
    def __setitem__(self, key: Literal["refiner_start"], value: float) -> None: ...
    @override
    def __setitem__(self, key: RefinerConfigKey, value: object) -> None:
        self._d[key] = value

    @overload
    def __getitem__(self, key: Literal["refiner_model"]) -> str | None: ...
    @overload
    def __getitem__(self, key: Literal["refiner_start"]) -> float: ...
    @override
    def __getitem__(self, key: RefinerConfigKey) -> object:
        return self._d[key]


class TiledConfig(GenConfig):
    def __init__(
        self,
        tiled_decoding: bool | None = False,
        decoding_tile_width: int | None = 10,
        decoding_tile_height: int | None = 10,
        decoding_tile_overlap: int | None = 2,
        tiled_diffusion: bool | None = False,
        diffusion_tile_width: int | None = 16,
        diffusion_tile_height: int | None = 16,
        diffusion_tile_overlap: int | None = 2,
    ):
        kwargs = {k: v for k, v in locals().items() if k != "self" and v is not None}

        super().__init__(**kwargs)

    @overload
    def __setitem__(
        self, key: Literal["tiled_decoding", "tiled_diffusion"], value: bool
    ) -> None: ...
    @overload
    def __setitem__(self, key: TiledConfigIntKey, value: int) -> None: ...
    @override
    def __setitem__(self, key: TiledConfigKey, value: object) -> None:
        self._d[key] = value

    @overload
    def __getitem__(
        self, key: Literal["tiled_decoding", "tiled_diffusion"]
    ) -> bool: ...
    @overload
    def __getitem__(self, key: TiledConfigIntKey) -> int: ...
    @override
    def __getitem__(self, key: TiledConfigKey) -> object:
        return self._d[key]


c = CoreConfig(width=1024, height=1024, model="model")
c["model"] = "what"
