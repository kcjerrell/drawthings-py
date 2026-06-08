from collections.abc import MutableMapping, Iterator
from typing import Unpack, overload, Literal, TypedDict, cast, TypeAlias
from typing_extensions import override
from drawthings_py.configs.types import LoraDict, SeedMode, CompressionMethod, UpscalerModel, SamplerType


ConfigValue: TypeAlias = (
    bool |
    CompressionMethod |
    float |
    int |
    list[LoraDict] |
    SamplerType |
    SeedMode |
    str |
    UpscalerModel
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
    width: int
    height: int
    seed: int
    steps: int
    guidance: float
    strength: float
    model: str | None
    sampler: SamplerType
    loras: list[LoraDict]
    batch_count: int
    batch_size: int
    hires_fix: bool
    hires_fix_width: int
    hires_fix_height: int
    hires_fix_strength: float
    upscaler: UpscalerModel | None
    image_guidance_scale: float
    seed_mode: SeedMode
    clip_skip: int
    mask_blur: float
    face_restoration: str | None
    decode_with_attention: bool
    hires_fix_decode_with_attention: bool
    clip_weight: float
    negative_prompt_for_image_prior: bool
    image_prior_steps: int
    refiner_model: str | None
    original_image_height: int
    original_image_width: int
    crop_top: int
    crop_left: int
    target_image_height: int
    target_image_width: int
    aesthetic_score: float
    negative_aesthetic_score: float
    zero_negative_prompt: bool
    refiner_start: float
    negative_original_image_height: int
    negative_original_image_width: int
    name: str | None
    fps: int
    motion_scale: int
    guiding_frame_noise: float
    guiding_frame_guidance: float
    num_frames: int
    mask_blur_outset: int
    sharpness: float
    shift: float
    stage_2_steps: int
    stage_2_cfg: float
    stage_2_shift: float
    tiled_decoding: bool
    decoding_tile_width: int
    decoding_tile_height: int
    decoding_tile_overlap: int
    stochastic_sampling_gamma: float
    preserve_original_after_inpaint: bool
    tiled_diffusion: bool
    diffusion_tile_width: int
    diffusion_tile_height: int
    diffusion_tile_overlap: int
    upscaler_scale_factor: int
    t5_text_encoder: bool
    separate_clip_l: bool
    clip_l_text: str | None
    separate_open_clip_g: bool
    open_clip_g_text: str | None
    speed_up_with_guidance_embed: bool
    guidance_embed: float
    resolution_dependent_shift: bool
    tea_cache_start: int
    tea_cache_end: int
    tea_cache_threshold: float
    tea_cache: bool
    separate_t5: bool
    t5_text: str | None
    tea_cache_max_skip_steps: int
    causal_inference_enabled: bool
    causal_inference: int
    causal_inference_pad: int
    cfg_zero_star: bool
    cfg_zero_init_steps: int
    compression_artifacts: CompressionMethod
    compression_artifacts_quality: float


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
    def __setitem__(self, key: Literal["upscaler"], value: UpscalerModel | None) -> None: ...
    @overload
    def __setitem__(self, key: Literal["seed_mode"], value: SeedMode) -> None: ...
    @overload
    def __setitem__(self, key: Literal["compression_artifacts"], value: CompressionMethod) -> None: ...
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
    def __getitem__(self, key: Literal["compression_artifacts"]) -> CompressionMethod: ...
    @override
    def __getitem__(self, key: GenConfigKey) -> object:
        return self._d[key]

    @property
    def id(self) -> int:
        """id"""
        return self._d.get("id", 0)
    @id.setter
    def id(self, value: int):
        self._d["id"] = value
    @property
    def width(self) -> int:
        """Width of the image in pixels (will be rounded to the nearest 64)"""
        return self._d.get("width", 0)
    @width.setter
    def width(self, value: int):
        self._d["width"] = value
    @property
    def height(self) -> int:
        """Height of the image in pixels (will be rounded to the nearest 64)"""
        return self._d.get("height", 0)
    @height.setter
    def height(self, value: int):
        self._d["height"] = value
    @property
    def seed(self) -> int:
        """controls the random number generation for the diffusion process, enabling reproducible image outputs when the same seed is used with identical parameters"""
        return self._d.get("seed", -1)
    @seed.setter
    def seed(self, value: int):
        self._d["seed"] = value
    @property
    def steps(self) -> int:
        """specifies the number of sampling iterations (denoising steps) performed during the image generation process"""
        return self._d.get("steps", 0)
    @steps.setter
    def steps(self, value: int):
        self._d["steps"] = value
    @property
    def guidance(self) -> float:
        """controls how strongly the generation follows the text prompt (also called CFG or text guidance)"""
        return self._d.get("guidance", 4.5)
    @guidance.setter
    def guidance(self, value: float):
        self._d["guidance"] = value
    @property
    def strength(self) -> float:
        """determines the denoising strength for img2img operations"""
        return self._d.get("strength", 0.0)
    @strength.setter
    def strength(self, value: float):
        self._d["strength"] = value
    @property
    def model(self) -> str | None:
        """specifies which model file to use for generation"""
        return self._d.get("model", None)
    @model.setter
    def model(self, value: str | None):
        self._d["model"] = value
    @property
    def sampler(self) -> SamplerType:
        """specifies the sampling algorithm and schedule to use for generation"""
        return self._d.get("sampler", SamplerType.DPMPP2MKarras)
    @sampler.setter
    def sampler(self, value: SamplerType):
        self._d["sampler"] = value
    @property
    def loras(self) -> list[LoraDict]:
        """loras"""
        return self._d.get("loras", [])
    @loras.setter
    def loras(self, value: list[LoraDict]):
        self._d["loras"] = value
    @property
    def batch_count(self) -> int:
        """batch_count"""
        return self._d.get("batch_count", 1)
    @batch_count.setter
    def batch_count(self, value: int):
        self._d["batch_count"] = value
    @property
    def batch_size(self) -> int:
        """number of images to generate in a single batch"""
        return self._d.get("batch_size", 1)
    @batch_size.setter
    def batch_size(self, value: int):
        self._d["batch_size"] = value
    @property
    def hires_fix(self) -> bool:
        """enables high-resolution fix for generation. When enabled, image generation begins at a lower resoution, then switches to the full size at the specified point"""
        return self._d.get("hires_fix", False)
    @hires_fix.setter
    def hires_fix(self, value: bool):
        self._d["hires_fix"] = value
    @property
    def hires_fix_width(self) -> int:
        """width to use for the first-pass generation"""
        return self._d.get("hires_fix_width", 512)
    @hires_fix_width.setter
    def hires_fix_width(self, value: int):
        self._d["hires_fix_width"] = value
    @property
    def hires_fix_height(self) -> int:
        """height to use for the first-pass generation"""
        return self._d.get("hires_fix_height", 512)
    @hires_fix_height.setter
    def hires_fix_height(self, value: int):
        self._d["hires_fix_height"] = value
    @property
    def hires_fix_strength(self) -> float:
        """What percentage of steps are used in the full size generation"""
        return self._d.get("hires_fix_strength", 0.7)
    @hires_fix_strength.setter
    def hires_fix_strength(self, value: float):
        self._d["hires_fix_strength"] = value
    @property
    def upscaler(self) -> UpscalerModel | None:
        """specifies which upscaler model to use for generation"""
        return self._d.get("upscaler", None)
    @upscaler.setter
    def upscaler(self, value: UpscalerModel | None):
        self._d["upscaler"] = value
    @property
    def image_guidance_scale(self) -> float:
        """used with HiDream E-1 to determine how strongly the init image is followed Used with model version HiDream"""
        return self._d.get("image_guidance_scale", 1.5)
    @image_guidance_scale.setter
    def image_guidance_scale(self, value: float):
        self._d["image_guidance_scale"] = value
    @property
    def seed_mode(self) -> SeedMode:
        """specifies how seeds are used for batch generation"""
        return self._d.get("seed_mode", SeedMode.ScaleAlike)
    @seed_mode.setter
    def seed_mode(self, value: SeedMode):
        self._d["seed_mode"] = value
    @property
    def clip_skip(self) -> int:
        """clip_skip Used with model versions SD, SD2, SDXL and SDXL"""
        return self._d.get("clip_skip", 1)
    @clip_skip.setter
    def clip_skip(self, value: int):
        self._d["clip_skip"] = value
    @property
    def mask_blur(self) -> float:
        """mask_blur"""
        return self._d.get("mask_blur", 0.0)
    @mask_blur.setter
    def mask_blur(self, value: float):
        self._d["mask_blur"] = value
    @property
    def face_restoration(self) -> str | None:
        """face_restoration"""
        return self._d.get("face_restoration", None)
    @face_restoration.setter
    def face_restoration(self, value: str | None):
        self._d["face_restoration"] = value
    @property
    def decode_with_attention(self) -> bool:
        """decode_with_attention"""
        return self._d.get("decode_with_attention", True)
    @decode_with_attention.setter
    def decode_with_attention(self, value: bool):
        self._d["decode_with_attention"] = value
    @property
    def hires_fix_decode_with_attention(self) -> bool:
        """hires_fix_decode_with_attention"""
        return self._d.get("hires_fix_decode_with_attention", True)
    @hires_fix_decode_with_attention.setter
    def hires_fix_decode_with_attention(self, value: bool):
        self._d["hires_fix_decode_with_attention"] = value
    @property
    def clip_weight(self) -> float:
        """clip_weight"""
        return self._d.get("clip_weight", 1)
    @clip_weight.setter
    def clip_weight(self, value: float):
        self._d["clip_weight"] = value
    @property
    def negative_prompt_for_image_prior(self) -> bool:
        """negative_prompt_for_image_prior"""
        return self._d.get("negative_prompt_for_image_prior", True)
    @negative_prompt_for_image_prior.setter
    def negative_prompt_for_image_prior(self, value: bool):
        self._d["negative_prompt_for_image_prior"] = value
    @property
    def image_prior_steps(self) -> int:
        """image_prior_steps"""
        return self._d.get("image_prior_steps", 5)
    @image_prior_steps.setter
    def image_prior_steps(self, value: int):
        self._d["image_prior_steps"] = value
    @property
    def refiner_model(self) -> str | None:
        """refiner_model"""
        return self._d.get("refiner_model", None)
    @refiner_model.setter
    def refiner_model(self, value: str | None):
        self._d["refiner_model"] = value
    @property
    def original_image_height(self) -> int:
        """The original height before image cropped during training (will be rounded to the nearest 64) Used with model versions SDXL and SDXL"""
        return self._d.get("original_image_height", 0)
    @original_image_height.setter
    def original_image_height(self, value: int):
        self._d["original_image_height"] = value
    @property
    def original_image_width(self) -> int:
        """The original width before image cropped during training (will be rounded to the nearest 64) Used with model versions SDXL and SDXL"""
        return self._d.get("original_image_width", 0)
    @original_image_width.setter
    def original_image_width(self, value: int):
        self._d["original_image_width"] = value
    @property
    def crop_top(self) -> int:
        """The top crop offset before image cropped during training (will be rounded to the nearest 64) Used with model versions SDXL and SDXL"""
        return self._d.get("crop_top", 0)
    @crop_top.setter
    def crop_top(self, value: int):
        self._d["crop_top"] = value
    @property
    def crop_left(self) -> int:
        """The left crop offset before image cropped during training (will be rounded to the nearest 64) Used with model versions SDXL and SDXL"""
        return self._d.get("crop_left", 0)
    @crop_left.setter
    def crop_left(self, value: int):
        self._d["crop_left"] = value
    @property
    def target_image_height(self) -> int:
        """The target height after image cropped during training (will be rounded to the nearest 64) Used with model versions SDXL and SDXL"""
        return self._d.get("target_image_height", 0)
    @target_image_height.setter
    def target_image_height(self, value: int):
        self._d["target_image_height"] = value
    @property
    def target_image_width(self) -> int:
        """The target width after image cropped during training (will be rounded to the nearest 64) Used with model versions SDXL and SDXL"""
        return self._d.get("target_image_width", 0)
    @target_image_width.setter
    def target_image_width(self, value: int):
        self._d["target_image_width"] = value
    @property
    def aesthetic_score(self) -> float:
        """aesthetic_score"""
        return self._d.get("aesthetic_score", 6)
    @aesthetic_score.setter
    def aesthetic_score(self, value: float):
        self._d["aesthetic_score"] = value
    @property
    def negative_aesthetic_score(self) -> float:
        """negative_aesthetic_score"""
        return self._d.get("negative_aesthetic_score", 2.5)
    @negative_aesthetic_score.setter
    def negative_aesthetic_score(self, value: float):
        self._d["negative_aesthetic_score"] = value
    @property
    def zero_negative_prompt(self) -> bool:
        """zero_negative_prompt Used with model versions Flux.1, HiDream, Pixart, SD3, SD3 Large, SDXL, SDXL and SSD"""
        return self._d.get("zero_negative_prompt", False)
    @zero_negative_prompt.setter
    def zero_negative_prompt(self, value: bool):
        self._d["zero_negative_prompt"] = value
    @property
    def refiner_start(self) -> float:
        """refiner_start"""
        return self._d.get("refiner_start", 0.7)
    @refiner_start.setter
    def refiner_start(self, value: float):
        self._d["refiner_start"] = value
    @property
    def negative_original_image_height(self) -> int:
        """The negative original image height (will be rounded to the nearest 64) Used with model versions SDXL and SDXL"""
        return self._d.get("negative_original_image_height", 0)
    @negative_original_image_height.setter
    def negative_original_image_height(self, value: int):
        self._d["negative_original_image_height"] = value
    @property
    def negative_original_image_width(self) -> int:
        """The negative original image width (will be rounded to the nearest 64) Used with model versions SDXL and SDXL"""
        return self._d.get("negative_original_image_width", 0)
    @negative_original_image_width.setter
    def negative_original_image_width(self, value: int):
        self._d["negative_original_image_width"] = value
    @property
    def name(self) -> str | None:
        """name"""
        return self._d.get("name", None)
    @name.setter
    def name(self, value: str | None):
        self._d["name"] = value
    @property
    def fps(self) -> int:
        """fps Used with model version SVD"""
        return self._d.get("fps", 5)
    @fps.setter
    def fps(self, value: int):
        self._d["fps"] = value
    @property
    def motion_scale(self) -> int:
        """motion_scale Used with model version SVD"""
        return self._d.get("motion_scale", 127)
    @motion_scale.setter
    def motion_scale(self, value: int):
        self._d["motion_scale"] = value
    @property
    def guiding_frame_noise(self) -> float:
        """guiding_frame_noise Used with model version SVD"""
        return self._d.get("guiding_frame_noise", 0.02)
    @guiding_frame_noise.setter
    def guiding_frame_noise(self, value: float):
        self._d["guiding_frame_noise"] = value
    @property
    def guiding_frame_guidance(self) -> float:
        """guiding_frame_guidance Used with model version SVD"""
        return self._d.get("guiding_frame_guidance", 1.0)
    @guiding_frame_guidance.setter
    def guiding_frame_guidance(self, value: float):
        self._d["guiding_frame_guidance"] = value
    @property
    def num_frames(self) -> int:
        """num_frames Used with model versions Hunyuan Video, LTX2, SVD, Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
        return self._d.get("num_frames", 14)
    @num_frames.setter
    def num_frames(self, value: int):
        self._d["num_frames"] = value
    @property
    def mask_blur_outset(self) -> int:
        """mask_blur_outset"""
        return self._d.get("mask_blur_outset", 0)
    @mask_blur_outset.setter
    def mask_blur_outset(self, value: int):
        self._d["mask_blur_outset"] = value
    @property
    def sharpness(self) -> float:
        """sharpness"""
        return self._d.get("sharpness", 0)
    @sharpness.setter
    def sharpness(self, value: float):
        self._d["sharpness"] = value
    @property
    def shift(self) -> float:
        """shift"""
        return self._d.get("shift", 1.0)
    @shift.setter
    def shift(self, value: float):
        self._d["shift"] = value
    @property
    def stage_2_steps(self) -> int:
        """stage_2_steps"""
        return self._d.get("stage_2_steps", 10)
    @stage_2_steps.setter
    def stage_2_steps(self, value: int):
        self._d["stage_2_steps"] = value
    @property
    def stage_2_cfg(self) -> float:
        """stage_2_cfg"""
        return self._d.get("stage_2_cfg", 1.0)
    @stage_2_cfg.setter
    def stage_2_cfg(self, value: float):
        self._d["stage_2_cfg"] = value
    @property
    def stage_2_shift(self) -> float:
        """stage_2_shift"""
        return self._d.get("stage_2_shift", 1.0)
    @stage_2_shift.setter
    def stage_2_shift(self, value: float):
        self._d["stage_2_shift"] = value
    @property
    def tiled_decoding(self) -> bool:
        """tiled_decoding"""
        return self._d.get("tiled_decoding", False)
    @tiled_decoding.setter
    def tiled_decoding(self, value: bool):
        self._d["tiled_decoding"] = value
    @property
    def decoding_tile_width(self) -> int:
        """The width of each tile for tiled decoding (will be rounded to the nearest 64)"""
        return self._d.get("decoding_tile_width", 10)
    @decoding_tile_width.setter
    def decoding_tile_width(self, value: int):
        self._d["decoding_tile_width"] = value
    @property
    def decoding_tile_height(self) -> int:
        """The height of each tile for tiled decoding (will be rounded to the nearest 64)"""
        return self._d.get("decoding_tile_height", 10)
    @decoding_tile_height.setter
    def decoding_tile_height(self, value: int):
        self._d["decoding_tile_height"] = value
    @property
    def decoding_tile_overlap(self) -> int:
        """The overlap between tiles for tiled decoding (will be rounded to the nearest 64)"""
        return self._d.get("decoding_tile_overlap", 2)
    @decoding_tile_overlap.setter
    def decoding_tile_overlap(self, value: int):
        self._d["decoding_tile_overlap"] = value
    @property
    def stochastic_sampling_gamma(self) -> float:
        """stochastic_sampling_gamma"""
        return self._d.get("stochastic_sampling_gamma", 0.3)
    @stochastic_sampling_gamma.setter
    def stochastic_sampling_gamma(self, value: float):
        self._d["stochastic_sampling_gamma"] = value
    @property
    def preserve_original_after_inpaint(self) -> bool:
        """preserve_original_after_inpaint"""
        return self._d.get("preserve_original_after_inpaint", True)
    @preserve_original_after_inpaint.setter
    def preserve_original_after_inpaint(self, value: bool):
        self._d["preserve_original_after_inpaint"] = value
    @property
    def tiled_diffusion(self) -> bool:
        """tiled_diffusion"""
        return self._d.get("tiled_diffusion", False)
    @tiled_diffusion.setter
    def tiled_diffusion(self, value: bool):
        self._d["tiled_diffusion"] = value
    @property
    def diffusion_tile_width(self) -> int:
        """The width of each tile for tiled diffusion (will be rounded to the nearest 64)"""
        return self._d.get("diffusion_tile_width", 16)
    @diffusion_tile_width.setter
    def diffusion_tile_width(self, value: int):
        self._d["diffusion_tile_width"] = value
    @property
    def diffusion_tile_height(self) -> int:
        """The height of each tile for tiled diffusion (will be rounded to the nearest 64)"""
        return self._d.get("diffusion_tile_height", 16)
    @diffusion_tile_height.setter
    def diffusion_tile_height(self, value: int):
        self._d["diffusion_tile_height"] = value
    @property
    def diffusion_tile_overlap(self) -> int:
        """The overlap between tiles for tiled diffusion (will be rounded to the nearest 64)"""
        return self._d.get("diffusion_tile_overlap", 2)
    @diffusion_tile_overlap.setter
    def diffusion_tile_overlap(self, value: int):
        self._d["diffusion_tile_overlap"] = value
    @property
    def upscaler_scale_factor(self) -> int:
        """upscaler_scale_factor"""
        return self._d.get("upscaler_scale_factor", 0)
    @upscaler_scale_factor.setter
    def upscaler_scale_factor(self, value: int):
        self._d["upscaler_scale_factor"] = value
    @property
    def t5_text_encoder(self) -> bool:
        """t5_text_encoder Used with model versions SD3 and SD3 Large"""
        return self._d.get("t5_text_encoder", True)
    @t5_text_encoder.setter
    def t5_text_encoder(self, value: bool):
        self._d["t5_text_encoder"] = value
    @property
    def separate_clip_l(self) -> bool:
        """separate_clip_l Used with model versions Flux.1, HiDream, SD3 and SD3 Large"""
        return self._d.get("separate_clip_l", False)
    @separate_clip_l.setter
    def separate_clip_l(self, value: bool):
        self._d["separate_clip_l"] = value
    @property
    def clip_l_text(self) -> str | None:
        """clip_l_text Used with model versions Flux.1, HiDream, SD3 and SD3 Large"""
        return self._d.get("clip_l_text", None)
    @clip_l_text.setter
    def clip_l_text(self, value: str | None):
        self._d["clip_l_text"] = value
    @property
    def separate_open_clip_g(self) -> bool:
        """separate_open_clip_g Used with model versions HiDream, SD3 and SD3 Large"""
        return self._d.get("separate_open_clip_g", False)
    @separate_open_clip_g.setter
    def separate_open_clip_g(self, value: bool):
        self._d["separate_open_clip_g"] = value
    @property
    def open_clip_g_text(self) -> str | None:
        """open_clip_g_text Used with model versions HiDream, SD3 and SD3 Large"""
        return self._d.get("open_clip_g_text", None)
    @open_clip_g_text.setter
    def open_clip_g_text(self, value: str | None):
        self._d["open_clip_g_text"] = value
    @property
    def speed_up_with_guidance_embed(self) -> bool:
        """speed_up_with_guidance_embed Used with model versions Flux.1, Flux.2, HiDream and Hunyuan Video"""
        return self._d.get("speed_up_with_guidance_embed", True)
    @speed_up_with_guidance_embed.setter
    def speed_up_with_guidance_embed(self, value: bool):
        self._d["speed_up_with_guidance_embed"] = value
    @property
    def guidance_embed(self) -> float:
        """guidance_embed Used with model versions Flux.1, Flux.2, HiDream and Hunyuan Video"""
        return self._d.get("guidance_embed", 3.5)
    @guidance_embed.setter
    def guidance_embed(self, value: float):
        self._d["guidance_embed"] = value
    @property
    def resolution_dependent_shift(self) -> bool:
        """resolution_dependent_shift Used with model versions Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Qwen, SD3, SD3 Large, Z Image and Cosmos2.5"""
        return self._d.get("resolution_dependent_shift", True)
    @resolution_dependent_shift.setter
    def resolution_dependent_shift(self, value: bool):
        self._d["resolution_dependent_shift"] = value
    @property
    def tea_cache_start(self) -> int:
        """tea_cache_start Used with model versions Flux.1, Hunyuan Video, Wan 2.1 and Wan 2.1"""
        return self._d.get("tea_cache_start", 5)
    @tea_cache_start.setter
    def tea_cache_start(self, value: int):
        self._d["tea_cache_start"] = value
    @property
    def tea_cache_end(self) -> int:
        """tea_cache_end Used with model versions Flux.1, Hunyuan Video, Wan 2.1 and Wan 2.1"""
        return self._d.get("tea_cache_end", -1)
    @tea_cache_end.setter
    def tea_cache_end(self, value: int):
        self._d["tea_cache_end"] = value
    @property
    def tea_cache_threshold(self) -> float:
        """tea_cache_threshold Used with model versions Flux.1, Hunyuan Video, Wan 2.1 and Wan 2.1"""
        return self._d.get("tea_cache_threshold", 0.06)
    @tea_cache_threshold.setter
    def tea_cache_threshold(self, value: float):
        self._d["tea_cache_threshold"] = value
    @property
    def tea_cache(self) -> bool:
        """tea_cache Used with model versions Flux.1, Hunyuan Video, Wan 2.1 and Wan 2.1"""
        return self._d.get("tea_cache", False)
    @tea_cache.setter
    def tea_cache(self, value: bool):
        self._d["tea_cache"] = value
    @property
    def separate_t5(self) -> bool:
        """separate_t5 Used with model version HiDream"""
        return self._d.get("separate_t5", False)
    @separate_t5.setter
    def separate_t5(self, value: bool):
        self._d["separate_t5"] = value
    @property
    def t5_text(self) -> str | None:
        """t5_text Used with model version HiDream"""
        return self._d.get("t5_text", None)
    @t5_text.setter
    def t5_text(self, value: str | None):
        self._d["t5_text"] = value
    @property
    def tea_cache_max_skip_steps(self) -> int:
        """tea_cache_max_skip_steps Used with model versions Flux.1, Hunyuan Video, Wan 2.1 and Wan 2.1"""
        return self._d.get("tea_cache_max_skip_steps", 3)
    @tea_cache_max_skip_steps.setter
    def tea_cache_max_skip_steps(self, value: int):
        self._d["tea_cache_max_skip_steps"] = value
    @property
    def causal_inference_enabled(self) -> bool:
        """causal_inference_enabled Used with model versions Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
        return self._d.get("causal_inference_enabled", False)
    @causal_inference_enabled.setter
    def causal_inference_enabled(self, value: bool):
        self._d["causal_inference_enabled"] = value
    @property
    def causal_inference(self) -> int:
        """causal_inference Used with model versions Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
        return self._d.get("causal_inference", 3)
    @causal_inference.setter
    def causal_inference(self, value: int):
        self._d["causal_inference"] = value
    @property
    def causal_inference_pad(self) -> int:
        """causal_inference_pad Used with model versions Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
        return self._d.get("causal_inference_pad", 0)
    @causal_inference_pad.setter
    def causal_inference_pad(self, value: int):
        self._d["causal_inference_pad"] = value
    @property
    def cfg_zero_star(self) -> bool:
        """cfg_zero_star Used with model versions Auraflow, Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Hunyuan Video, LTX2, Qwen, SD3, SD3 Large, Wan 2.1, Wan 2.1, Wan 2.2 5b, Z Image, Ernie Image and Cosmos2.5"""
        return self._d.get("cfg_zero_star", False)
    @cfg_zero_star.setter
    def cfg_zero_star(self, value: bool):
        self._d["cfg_zero_star"] = value
    @property
    def cfg_zero_init_steps(self) -> int:
        """cfg_zero_init_steps Used with model versions Auraflow, Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Hunyuan Video, LTX2, Qwen, SD3, SD3 Large, Wan 2.1, Wan 2.1, Wan 2.2 5b, Z Image, Ernie Image and Cosmos2.5"""
        return self._d.get("cfg_zero_init_steps", 0)
    @cfg_zero_init_steps.setter
    def cfg_zero_init_steps(self, value: int):
        self._d["cfg_zero_init_steps"] = value
    @property
    def compression_artifacts(self) -> CompressionMethod:
        """compression_artifacts Used with model versions Hunyuan Video, LTX2, Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
        return self._d.get("compression_artifacts", CompressionMethod.Disabled)
    @compression_artifacts.setter
    def compression_artifacts(self, value: CompressionMethod):
        self._d["compression_artifacts"] = value
    @property
    def compression_artifacts_quality(self) -> float:
        """compression_artifacts_quality Used with model versions Hunyuan Video, LTX2, Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
        return self._d.get("compression_artifacts_quality", 43.1)
    @compression_artifacts_quality.setter
    def compression_artifacts_quality(self, value: float):
        self._d["compression_artifacts_quality"] = value


class CoreConfig(GenConfig):
    def __init__(self, 
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
        kwargs = {
            k: v
            for k, v in locals().items()
            if k != "self" and v is not None
        }

        super().__init__(**kwargs)

    @overload
    def __setitem__(self, key: CoreConfigIntKey, value: int) -> None: ...
    @overload
    def __setitem__(self, key: Literal["guidance", "strength", "shift"], value: float) -> None: ...
    @overload
    def __setitem__(self, key: Literal["model"], value: str | None) -> None: ...
    @overload
    def __setitem__(self, key: Literal["sampler"], value: SamplerType) -> None: ...
    @overload
    def __setitem__(self, key: Literal["loras"], value: list[LoraDict]) -> None: ...
    @overload
    def __setitem__(self, key: Literal["resolution_dependent_shift"], value: bool) -> None: ...
    @override
    def __setitem__(self, key: CoreConfigKey, value: object) -> None: # pyright: ignore[reportIncompatibleMethodOverride]
        self._d[key] = value # pyright: ignore[reportGeneralTypeIssues]

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
    def __getitem__(self, key: CoreConfigKey) -> object: # pyright: ignore[reportIncompatibleMethodOverride]
        return self._d[key] # pyright: ignore[reportTypedDictNotRequiredAccess]

    


class ExtraConfig(GenConfig):
    def __init__(self, 
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
        kwargs = {
            k: v
            for k, v in locals().items()
            if k != "self" and v is not None
        }

        super().__init__(**kwargs)

    @overload
    def __setitem__(self, key: ExtraConfigIntKey, value: int) -> None: ...
    @overload
    def __setitem__(self, key: ExtraConfigFloatKey, value: float) -> None: ...
    @overload
    def __setitem__(self, key: Literal["seed_mode"], value: SeedMode) -> None: ...
    @overload
    def __setitem__(self, key: Literal["face_restoration"], value: str | None) -> None: ...
    @overload
    def __setitem__(self, key: Literal["zero_negative_prompt", "preserve_original_after_inpaint"], value: bool) -> None: ...
    @override
    def __setitem__(self, key: ExtraConfigKey, value: object) -> None: # pyright: ignore[reportIncompatibleMethodOverride]
        self._d[key] = value # pyright: ignore[reportGeneralTypeIssues]

    @overload
    def __getitem__(self, key: ExtraConfigIntKey) -> int: ...
    @overload
    def __getitem__(self, key: ExtraConfigFloatKey) -> float: ...
    @overload
    def __getitem__(self, key: Literal["seed_mode"]) -> SeedMode: ...
    @overload
    def __getitem__(self, key: Literal["face_restoration"]) -> str | None: ...
    @overload
    def __getitem__(self, key: Literal["zero_negative_prompt", "preserve_original_after_inpaint"]) -> bool: ...
    @override
    def __getitem__(self, key: ExtraConfigKey) -> object: # pyright: ignore[reportIncompatibleMethodOverride]
        return self._d[key] # pyright: ignore[reportTypedDictNotRequiredAccess]

    


class HiResFixConfig(GenConfig):
    def __init__(self, 
        hires_fix: bool | None = False,
        hires_fix_width: int | None = 512,
        hires_fix_height: int | None = 512,
        hires_fix_strength: float | None = 0.7,
    ):
        kwargs = {
            k: v
            for k, v in locals().items()
            if k != "self" and v is not None
        }

        super().__init__(**kwargs)

    @overload
    def __setitem__(self, key: Literal["hires_fix"], value: bool) -> None: ...
    @overload
    def __setitem__(self, key: Literal["hires_fix_width", "hires_fix_height"], value: int) -> None: ...
    @overload
    def __setitem__(self, key: Literal["hires_fix_strength"], value: float) -> None: ...
    @override
    def __setitem__(self, key: HiResFixConfigKey, value: object) -> None: # pyright: ignore[reportIncompatibleMethodOverride]
        self._d[key] = value # pyright: ignore[reportGeneralTypeIssues]

    @overload
    def __getitem__(self, key: Literal["hires_fix"]) -> bool: ...
    @overload
    def __getitem__(self, key: Literal["hires_fix_width", "hires_fix_height"]) -> int: ...
    @overload
    def __getitem__(self, key: Literal["hires_fix_strength"]) -> float: ...
    @override
    def __getitem__(self, key: HiResFixConfigKey) -> object: # pyright: ignore[reportIncompatibleMethodOverride]
        return self._d[key] # pyright: ignore[reportTypedDictNotRequiredAccess]

    


class UpscalerConfig(GenConfig):
    def __init__(self, 
        upscaler: UpscalerModel | None | None = None,
        upscaler_scale_factor: int | None = 0,
    ):
        kwargs = {
            k: v
            for k, v in locals().items()
            if k != "self" and v is not None
        }

        super().__init__(**kwargs)

    @overload
    def __setitem__(self, key: Literal["upscaler"], value: UpscalerModel | None) -> None: ...
    @overload
    def __setitem__(self, key: Literal["upscaler_scale_factor"], value: int) -> None: ...
    @override
    def __setitem__(self, key: UpscalerConfigKey, value: object) -> None: # pyright: ignore[reportIncompatibleMethodOverride]
        self._d[key] = value # pyright: ignore[reportGeneralTypeIssues]

    @overload
    def __getitem__(self, key: Literal["upscaler"]) -> UpscalerModel | None: ...
    @overload
    def __getitem__(self, key: Literal["upscaler_scale_factor"]) -> int: ...
    @override
    def __getitem__(self, key: UpscalerConfigKey) -> object: # pyright: ignore[reportIncompatibleMethodOverride]
        return self._d[key] # pyright: ignore[reportTypedDictNotRequiredAccess]

    


class RefinerConfig(GenConfig):
    def __init__(self, 
        refiner_model: str | None | None = None,
        refiner_start: float | None = 0.7,
    ):
        kwargs = {
            k: v
            for k, v in locals().items()
            if k != "self" and v is not None
        }

        super().__init__(**kwargs)

    @overload
    def __setitem__(self, key: Literal["refiner_model"], value: str | None) -> None: ...
    @overload
    def __setitem__(self, key: Literal["refiner_start"], value: float) -> None: ...
    @override
    def __setitem__(self, key: RefinerConfigKey, value: object) -> None: # pyright: ignore[reportIncompatibleMethodOverride]
        self._d[key] = value # pyright: ignore[reportGeneralTypeIssues]

    @overload
    def __getitem__(self, key: Literal["refiner_model"]) -> str | None: ...
    @overload
    def __getitem__(self, key: Literal["refiner_start"]) -> float: ...
    @override
    def __getitem__(self, key: RefinerConfigKey) -> object: # pyright: ignore[reportIncompatibleMethodOverride]
        return self._d[key] # pyright: ignore[reportTypedDictNotRequiredAccess]

    


class TiledConfig(GenConfig):
    def __init__(self, 
        tiled_decoding: bool | None = False,
        decoding_tile_width: int | None = 10,
        decoding_tile_height: int | None = 10,
        decoding_tile_overlap: int | None = 2,
        tiled_diffusion: bool | None = False,
        diffusion_tile_width: int | None = 16,
        diffusion_tile_height: int | None = 16,
        diffusion_tile_overlap: int | None = 2,
    ):
        kwargs = {
            k: v
            for k, v in locals().items()
            if k != "self" and v is not None
        }

        super().__init__(**kwargs)

    @overload
    def __setitem__(self, key: Literal["tiled_decoding", "tiled_diffusion"], value: bool) -> None: ...
    @overload
    def __setitem__(self, key: TiledConfigIntKey, value: int) -> None: ...
    @override
    def __setitem__(self, key: TiledConfigKey, value: object) -> None: # pyright: ignore[reportIncompatibleMethodOverride]
        self._d[key] = value # pyright: ignore[reportGeneralTypeIssues]

    @overload
    def __getitem__(self, key: Literal["tiled_decoding", "tiled_diffusion"]) -> bool: ...
    @overload
    def __getitem__(self, key: TiledConfigIntKey) -> int: ...
    @override
    def __getitem__(self, key: TiledConfigKey) -> object: # pyright: ignore[reportIncompatibleMethodOverride]
        return self._d[key] # pyright: ignore[reportTypedDictNotRequiredAccess]

    


