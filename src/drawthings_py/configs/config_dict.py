from collections.abc import MutableMapping

from typing_extensions import override

from .types import UpscalerModel, CompressionMethod, LoraDict, SeedMode, SamplerType
from typing import Any, Iterator, Literal, TypedDict, Unpack, overload


class ConfigDict(TypedDict, total=False):
    speed_up_with_guidance_embed: bool
    """speed_up_with_guidance_embed Used with model versions Flux.1, Flux.2, HiDream and Hunyuan Video"""
    guiding_frame_guidance: float
    """guiding_frame_guidance Used with model version SVD"""
    tea_cache_max_skip_steps: int
    """tea_cache_max_skip_steps Used with model versions Flux.1, Hunyuan Video, Wan 2.1 and Wan 2.1"""
    fps: int
    """fps Used with model version SVD"""
    negative_original_image_height: int
    """The negative original image height (will be rounded to the nearest 64) Used with model versions SDXL and SDXL"""
    decoding_tile_height: int
    """The height of each tile for tiled decoding (will be rounded to the nearest 64)"""
    stage_2_shift: float
    """stage_2_shift"""
    open_clip_g_text: str | None
    """open_clip_g_text Used with model versions HiDream, SD3 and SD3 Large"""
    clip_weight: float
    """clip_weight"""
    causal_inference_pad: int
    """causal_inference_pad Used with model versions Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
    motion_scale: int
    """motion_scale Used with model version SVD"""
    refiner_model: str | None
    """refiner_model"""
    stage_2_steps: int
    """stage_2_steps"""
    hires_fix_height: int
    """height to use for the first-pass generation"""
    batch_size: int
    """number of images to generate in a single batch"""
    aesthetic_score: float
    """aesthetic_score"""
    original_image_width: int
    """The original width before image cropped during training (will be rounded to the nearest 64) Used with model versions SDXL and SDXL"""
    sampler: SamplerType
    """specifies the sampling algorithm and schedule to use for generation"""
    upscaler: UpscalerModel | None
    """specifies which upscaler model to use for generation"""
    diffusion_tile_width: int
    """The width of each tile for tiled diffusion (will be rounded to the nearest 64)"""
    height: int
    """Height of the image in pixels (will be rounded to the nearest 64)"""
    hires_fix_strength: float
    """What percentage of steps are used in the full size generation"""
    tea_cache: bool
    """tea_cache Used with model versions Flux.1, Hunyuan Video, Wan 2.1 and Wan 2.1"""
    tea_cache_start: int
    """tea_cache_start Used with model versions Flux.1, Hunyuan Video, Wan 2.1 and Wan 2.1"""
    crop_top: int
    """The top crop offset before image cropped during training (will be rounded to the nearest 64) Used with model versions SDXL and SDXL"""
    batch_count: int
    """batch_count"""
    diffusion_tile_overlap: int
    """The overlap between tiles for tiled diffusion (will be rounded to the nearest 64)"""
    negative_prompt_for_image_prior: bool
    """negative_prompt_for_image_prior"""
    image_guidance_scale: float
    """used with HiDream E-1 to determine how strongly the init image is followed Used with model version HiDream"""
    clip_skip: int
    """clip_skip Used with model versions SD, SD2, SDXL and SDXL"""
    mask_blur_outset: int
    """mask_blur_outset"""
    diffusion_tile_height: int
    """The height of each tile for tiled diffusion (will be rounded to the nearest 64)"""
    separate_t5: bool
    """separate_t5 Used with model version HiDream"""
    guidance_embed: float
    """guidance_embed Used with model versions Flux.1, Flux.2, HiDream and Hunyuan Video"""
    num_frames: int
    """num_frames Used with model versions Hunyuan Video, LTX2, SVD, Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
    compression_artifacts_quality: float
    """compression_artifacts_quality Used with model versions Hunyuan Video, LTX2, Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
    decoding_tile_overlap: int
    """The overlap between tiles for tiled decoding (will be rounded to the nearest 64)"""
    negative_original_image_width: int
    """The negative original image width (will be rounded to the nearest 64) Used with model versions SDXL and SDXL"""
    t5_text_encoder: bool
    """t5_text_encoder Used with model versions SD3 and SD3 Large"""
    face_restoration: str | None
    """face_restoration"""
    guidance: float
    """controls how strongly the generation follows the text prompt (also called CFG or text guidance)"""
    cfg_zero_star: bool
    """cfg_zero_star Used with model versions Auraflow, Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Hunyuan Video, LTX2, Qwen, SD3, SD3 Large, Wan 2.1, Wan 2.1, Wan 2.2 5b, Z Image, Ernie Image and Cosmos2.5"""
    stage_2_cfg: float
    """stage_2_cfg"""
    loras: list[LoraDict]
    """loras"""
    hires_fix_decode_with_attention: bool
    """hires_fix_decode_with_attention"""
    strength: float
    """determines the denoising strength for img2img operations"""
    zero_negative_prompt: bool
    """zero_negative_prompt Used with model versions Flux.1, HiDream, Pixart, SD3, SD3 Large, SDXL, SDXL and SSD"""
    tea_cache_threshold: float
    """tea_cache_threshold Used with model versions Flux.1, Hunyuan Video, Wan 2.1 and Wan 2.1"""
    width: int
    """Width of the image in pixels (will be rounded to the nearest 64)"""
    id: int
    """id"""
    tea_cache_end: int
    """tea_cache_end Used with model versions Flux.1, Hunyuan Video, Wan 2.1 and Wan 2.1"""
    name: str | None
    """name"""
    hires_fix_width: int
    """width to use for the first-pass generation"""
    decode_with_attention: bool
    """decode_with_attention"""
    guiding_frame_noise: float
    """guiding_frame_noise Used with model version SVD"""
    tiled_diffusion: bool
    """tiled_diffusion"""
    upscaler_scale_factor: int
    """upscaler_scale_factor"""
    separate_clip_l: bool
    """separate_clip_l Used with model versions Flux.1, HiDream, SD3 and SD3 Large"""
    crop_left: int
    """The left crop offset before image cropped during training (will be rounded to the nearest 64) Used with model versions SDXL and SDXL"""
    image_prior_steps: int
    """image_prior_steps"""
    clip_l_text: str | None
    """clip_l_text Used with model versions Flux.1, HiDream, SD3 and SD3 Large"""
    tiled_decoding: bool
    """tiled_decoding"""
    causal_inference: int
    """causal_inference Used with model versions Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
    resolution_dependent_shift: bool
    """resolution_dependent_shift Used with model versions Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Qwen, SD3, SD3 Large, Z Image and Cosmos2.5"""
    negative_aesthetic_score: float
    """negative_aesthetic_score"""
    compression_artifacts: CompressionMethod
    """compression_artifacts Used with model versions Hunyuan Video, LTX2, Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
    shift: float
    """shift"""
    sharpness: float
    """sharpness"""
    hires_fix: bool
    """enables high-resolution fix for generation. When enabled, image generation begins at a lower resoution, then switches to the full size at the specified point"""
    t5_text: str | None
    """t5_text Used with model version HiDream"""
    target_image_width: int
    """The target width after image cropped during training (will be rounded to the nearest 64) Used with model versions SDXL and SDXL"""
    steps: int
    """specifies the number of sampling iterations (denoising steps) performed during the image generation process"""
    model: str | None
    """specifies which model file to use for generation"""
    separate_open_clip_g: bool
    """separate_open_clip_g Used with model versions HiDream, SD3 and SD3 Large"""
    causal_inference_enabled: bool
    """causal_inference_enabled Used with model versions Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
    seed: int
    """controls the random number generation for the diffusion process, enabling reproducible image outputs when the same seed is used with identical parameters"""
    decoding_tile_width: int
    """The width of each tile for tiled decoding (will be rounded to the nearest 64)"""
    cfg_zero_init_steps: int
    """cfg_zero_init_steps Used with model versions Auraflow, Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Hunyuan Video, LTX2, Qwen, SD3, SD3 Large, Wan 2.1, Wan 2.1, Wan 2.2 5b, Z Image, Ernie Image and Cosmos2.5"""
    preserve_original_after_inpaint: bool
    """preserve_original_after_inpaint"""
    target_image_height: int
    """The target height after image cropped during training (will be rounded to the nearest 64) Used with model versions SDXL and SDXL"""
    original_image_height: int
    """The original height before image cropped during training (will be rounded to the nearest 64) Used with model versions SDXL and SDXL"""
    refiner_start: float
    """refiner_start"""
    mask_blur: float
    """mask_blur"""
    stochastic_sampling_gamma: float
    """stochastic_sampling_gamma"""
    seed_mode: SeedMode
    """specifies how seeds are used for batch generation"""


class CoreConfig(TypedDict, total=False):
    loras: list[LoraDict]
    """loras"""
    strength: float
    """determines the denoising strength for img2img operations"""
    shift: float
    """shift"""
    sampler: SamplerType
    """specifies the sampling algorithm and schedule to use for generation"""
    seed: int
    """controls the random number generation for the diffusion process, enabling reproducible image outputs when the same seed is used with identical parameters"""
    width: int
    """Width of the image in pixels (will be rounded to the nearest 64)"""
    steps: int
    """specifies the number of sampling iterations (denoising steps) performed during the image generation process"""
    guidance: float
    """controls how strongly the generation follows the text prompt (also called CFG or text guidance)"""
    height: int
    """Height of the image in pixels (will be rounded to the nearest 64)"""
    model: str | None
    """specifies which model file to use for generation"""
    resolution_dependent_shift: bool
    """resolution_dependent_shift Used with model versions Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Qwen, SD3, SD3 Large, Z Image and Cosmos2.5"""

    @override
    def __or__(self, other: TypedDict) -> ConfigDict:
        return self | other


class ExtraConfig(TypedDict, total=False):
    zero_negative_prompt: bool
    """zero_negative_prompt Used with model versions Flux.1, HiDream, Pixart, SD3, SD3 Large, SDXL, SDXL and SSD"""
    mask_blur_outset: int
    """mask_blur_outset"""
    face_restoration: str | None
    """face_restoration"""
    clip_skip: int
    """clip_skip Used with model versions SD, SD2, SDXL and SDXL"""
    mask_blur: float
    """mask_blur"""
    sharpness: float
    """sharpness"""
    stochastic_sampling_gamma: float
    """stochastic_sampling_gamma"""
    num_frames: int
    """num_frames Used with model versions Hunyuan Video, LTX2, SVD, Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
    preserve_original_after_inpaint: bool
    """preserve_original_after_inpaint"""
    seed_mode: SeedMode
    """specifies how seeds are used for batch generation"""
    image_guidance_scale: float
    """used with HiDream E-1 to determine how strongly the init image is followed Used with model version HiDream"""
    batch_size: int
    """number of images to generate in a single batch"""

    @override
    def __or__(self, other: TypedDict) -> ConfigDict:
        return self | other


class HiResFixConfig(TypedDict, total=False):
    hires_fix_height: int
    """height to use for the first-pass generation"""
    hires_fix: bool
    """enables high-resolution fix for generation. When enabled, image generation begins at a lower resoution, then switches to the full size at the specified point"""
    hires_fix_strength: float
    """What percentage of steps are used in the full size generation"""
    hires_fix_width: int
    """width to use for the first-pass generation"""

    @override
    def __or__(self, other: TypedDict) -> ConfigDict:
        return self | other


class UpscalerConfig(TypedDict, total=False):
    upscaler: UpscalerModel | None
    """specifies which upscaler model to use for generation"""
    upscaler_scale_factor: int
    """upscaler_scale_factor"""


class HiDreamConfig(TypedDict, total=False):
    speed_up_with_guidance_embed: bool
    """speed_up_with_guidance_embed Used with model versions Flux.1, Flux.2, HiDream and Hunyuan Video"""
    separate_open_clip_g: bool
    """separate_open_clip_g Used with model versions HiDream, SD3 and SD3 Large"""
    zero_negative_prompt: bool
    """zero_negative_prompt Used with model versions Flux.1, HiDream, Pixart, SD3, SD3 Large, SDXL, SDXL and SSD"""
    separate_t5: bool
    """separate_t5 Used with model version HiDream"""
    separate_clip_l: bool
    """separate_clip_l Used with model versions Flux.1, HiDream, SD3 and SD3 Large"""
    guidance_embed: float
    """guidance_embed Used with model versions Flux.1, Flux.2, HiDream and Hunyuan Video"""
    cfg_zero_init_steps: int
    """cfg_zero_init_steps Used with model versions Auraflow, Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Hunyuan Video, LTX2, Qwen, SD3, SD3 Large, Wan 2.1, Wan 2.1, Wan 2.2 5b, Z Image, Ernie Image and Cosmos2.5"""
    image_guidance_scale: float
    """used with HiDream E-1 to determine how strongly the init image is followed Used with model version HiDream"""
    open_clip_g_text: str | None
    """open_clip_g_text Used with model versions HiDream, SD3 and SD3 Large"""
    clip_l_text: str | None
    """clip_l_text Used with model versions Flux.1, HiDream, SD3 and SD3 Large"""
    t5_text: str | None
    """t5_text Used with model version HiDream"""
    cfg_zero_star: bool
    """cfg_zero_star Used with model versions Auraflow, Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Hunyuan Video, LTX2, Qwen, SD3, SD3 Large, Wan 2.1, Wan 2.1, Wan 2.2 5b, Z Image, Ernie Image and Cosmos2.5"""
    resolution_dependent_shift: bool
    """resolution_dependent_shift Used with model versions Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Qwen, SD3, SD3 Large, Z Image and Cosmos2.5"""


class SD1And2Config(TypedDict, total=False):
    clip_skip: int
    """clip_skip Used with model versions SD, SD2, SDXL and SDXL"""


class SDXLConfig(TypedDict, total=False):
    crop_top: int
    """The top crop offset before image cropped during training (will be rounded to the nearest 64) Used with model versions SDXL and SDXL"""
    target_image_height: int
    """The target height after image cropped during training (will be rounded to the nearest 64) Used with model versions SDXL and SDXL"""
    target_image_width: int
    """The target width after image cropped during training (will be rounded to the nearest 64) Used with model versions SDXL and SDXL"""
    negative_original_image_width: int
    """The negative original image width (will be rounded to the nearest 64) Used with model versions SDXL and SDXL"""
    original_image_height: int
    """The original height before image cropped during training (will be rounded to the nearest 64) Used with model versions SDXL and SDXL"""
    zero_negative_prompt: bool
    """zero_negative_prompt Used with model versions Flux.1, HiDream, Pixart, SD3, SD3 Large, SDXL, SDXL and SSD"""
    clip_skip: int
    """clip_skip Used with model versions SD, SD2, SDXL and SDXL"""
    crop_left: int
    """The left crop offset before image cropped during training (will be rounded to the nearest 64) Used with model versions SDXL and SDXL"""
    negative_original_image_height: int
    """The negative original image height (will be rounded to the nearest 64) Used with model versions SDXL and SDXL"""
    original_image_width: int
    """The original width before image cropped during training (will be rounded to the nearest 64) Used with model versions SDXL and SDXL"""


class RefinerConfig(TypedDict, total=False):
    refiner_model: str | None
    """refiner_model"""
    refiner_start: float
    """refiner_start"""


class FluxConfig(TypedDict, total=False):
    speed_up_with_guidance_embed: bool
    """speed_up_with_guidance_embed Used with model versions Flux.1, Flux.2, HiDream and Hunyuan Video"""
    tea_cache_max_skip_steps: int
    """tea_cache_max_skip_steps Used with model versions Flux.1, Hunyuan Video, Wan 2.1 and Wan 2.1"""
    tea_cache_threshold: float
    """tea_cache_threshold Used with model versions Flux.1, Hunyuan Video, Wan 2.1 and Wan 2.1"""
    zero_negative_prompt: bool
    """zero_negative_prompt Used with model versions Flux.1, HiDream, Pixart, SD3, SD3 Large, SDXL, SDXL and SSD"""
    separate_clip_l: bool
    """separate_clip_l Used with model versions Flux.1, HiDream, SD3 and SD3 Large"""
    guidance_embed: float
    """guidance_embed Used with model versions Flux.1, Flux.2, HiDream and Hunyuan Video"""
    tea_cache_start: int
    """tea_cache_start Used with model versions Flux.1, Hunyuan Video, Wan 2.1 and Wan 2.1"""
    cfg_zero_init_steps: int
    """cfg_zero_init_steps Used with model versions Auraflow, Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Hunyuan Video, LTX2, Qwen, SD3, SD3 Large, Wan 2.1, Wan 2.1, Wan 2.2 5b, Z Image, Ernie Image and Cosmos2.5"""
    tea_cache_end: int
    """tea_cache_end Used with model versions Flux.1, Hunyuan Video, Wan 2.1 and Wan 2.1"""
    clip_l_text: str | None
    """clip_l_text Used with model versions Flux.1, HiDream, SD3 and SD3 Large"""
    cfg_zero_star: bool
    """cfg_zero_star Used with model versions Auraflow, Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Hunyuan Video, LTX2, Qwen, SD3, SD3 Large, Wan 2.1, Wan 2.1, Wan 2.2 5b, Z Image, Ernie Image and Cosmos2.5"""
    tea_cache: bool
    """tea_cache Used with model versions Flux.1, Hunyuan Video, Wan 2.1 and Wan 2.1"""
    resolution_dependent_shift: bool
    """resolution_dependent_shift Used with model versions Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Qwen, SD3, SD3 Large, Z Image and Cosmos2.5"""


class SD3Config(TypedDict, total=False):
    separate_open_clip_g: bool
    """separate_open_clip_g Used with model versions HiDream, SD3 and SD3 Large"""
    t5_text_encoder: bool
    """t5_text_encoder Used with model versions SD3 and SD3 Large"""
    zero_negative_prompt: bool
    """zero_negative_prompt Used with model versions Flux.1, HiDream, Pixart, SD3, SD3 Large, SDXL, SDXL and SSD"""
    separate_clip_l: bool
    """separate_clip_l Used with model versions Flux.1, HiDream, SD3 and SD3 Large"""
    cfg_zero_init_steps: int
    """cfg_zero_init_steps Used with model versions Auraflow, Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Hunyuan Video, LTX2, Qwen, SD3, SD3 Large, Wan 2.1, Wan 2.1, Wan 2.2 5b, Z Image, Ernie Image and Cosmos2.5"""
    open_clip_g_text: str | None
    """open_clip_g_text Used with model versions HiDream, SD3 and SD3 Large"""
    clip_l_text: str | None
    """clip_l_text Used with model versions Flux.1, HiDream, SD3 and SD3 Large"""
    cfg_zero_star: bool
    """cfg_zero_star Used with model versions Auraflow, Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Hunyuan Video, LTX2, Qwen, SD3, SD3 Large, Wan 2.1, Wan 2.1, Wan 2.2 5b, Z Image, Ernie Image and Cosmos2.5"""
    resolution_dependent_shift: bool
    """resolution_dependent_shift Used with model versions Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Qwen, SD3, SD3 Large, Z Image and Cosmos2.5"""


class SVDConfig(TypedDict, total=False):
    guiding_frame_guidance: float
    """guiding_frame_guidance Used with model version SVD"""
    fps: int
    """fps Used with model version SVD"""
    motion_scale: int
    """motion_scale Used with model version SVD"""
    num_frames: int
    """num_frames Used with model versions Hunyuan Video, LTX2, SVD, Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
    guiding_frame_noise: float
    """guiding_frame_noise Used with model version SVD"""


class HunyuanConfig(TypedDict, total=False):
    speed_up_with_guidance_embed: bool
    """speed_up_with_guidance_embed Used with model versions Flux.1, Flux.2, HiDream and Hunyuan Video"""
    compression_artifacts: CompressionMethod
    """compression_artifacts Used with model versions Hunyuan Video, LTX2, Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
    tea_cache_max_skip_steps: int
    """tea_cache_max_skip_steps Used with model versions Flux.1, Hunyuan Video, Wan 2.1 and Wan 2.1"""
    tea_cache_threshold: float
    """tea_cache_threshold Used with model versions Flux.1, Hunyuan Video, Wan 2.1 and Wan 2.1"""
    tea_cache_start: int
    """tea_cache_start Used with model versions Flux.1, Hunyuan Video, Wan 2.1 and Wan 2.1"""
    guidance_embed: float
    """guidance_embed Used with model versions Flux.1, Flux.2, HiDream and Hunyuan Video"""
    num_frames: int
    """num_frames Used with model versions Hunyuan Video, LTX2, SVD, Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
    cfg_zero_init_steps: int
    """cfg_zero_init_steps Used with model versions Auraflow, Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Hunyuan Video, LTX2, Qwen, SD3, SD3 Large, Wan 2.1, Wan 2.1, Wan 2.2 5b, Z Image, Ernie Image and Cosmos2.5"""
    compression_artifacts_quality: float
    """compression_artifacts_quality Used with model versions Hunyuan Video, LTX2, Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
    tea_cache_end: int
    """tea_cache_end Used with model versions Flux.1, Hunyuan Video, Wan 2.1 and Wan 2.1"""
    cfg_zero_star: bool
    """cfg_zero_star Used with model versions Auraflow, Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Hunyuan Video, LTX2, Qwen, SD3, SD3 Large, Wan 2.1, Wan 2.1, Wan 2.2 5b, Z Image, Ernie Image and Cosmos2.5"""
    tea_cache: bool
    """tea_cache Used with model versions Flux.1, Hunyuan Video, Wan 2.1 and Wan 2.1"""


class LTX2Config(TypedDict, total=False):
    compression_artifacts: CompressionMethod
    """compression_artifacts Used with model versions Hunyuan Video, LTX2, Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
    num_frames: int
    """num_frames Used with model versions Hunyuan Video, LTX2, SVD, Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
    compression_artifacts_quality: float
    """compression_artifacts_quality Used with model versions Hunyuan Video, LTX2, Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
    cfg_zero_init_steps: int
    """cfg_zero_init_steps Used with model versions Auraflow, Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Hunyuan Video, LTX2, Qwen, SD3, SD3 Large, Wan 2.1, Wan 2.1, Wan 2.2 5b, Z Image, Ernie Image and Cosmos2.5"""
    cfg_zero_star: bool
    """cfg_zero_star Used with model versions Auraflow, Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Hunyuan Video, LTX2, Qwen, SD3, SD3 Large, Wan 2.1, Wan 2.1, Wan 2.2 5b, Z Image, Ernie Image and Cosmos2.5"""


class WanConfig(TypedDict, total=False):
    compression_artifacts: CompressionMethod
    """compression_artifacts Used with model versions Hunyuan Video, LTX2, Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
    tea_cache_max_skip_steps: int
    """tea_cache_max_skip_steps Used with model versions Flux.1, Hunyuan Video, Wan 2.1 and Wan 2.1"""
    tea_cache_threshold: float
    """tea_cache_threshold Used with model versions Flux.1, Hunyuan Video, Wan 2.1 and Wan 2.1"""
    causal_inference_enabled: bool
    """causal_inference_enabled Used with model versions Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
    causal_inference: int
    """causal_inference Used with model versions Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
    tea_cache_start: int
    """tea_cache_start Used with model versions Flux.1, Hunyuan Video, Wan 2.1 and Wan 2.1"""
    num_frames: int
    """num_frames Used with model versions Hunyuan Video, LTX2, SVD, Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
    cfg_zero_init_steps: int
    """cfg_zero_init_steps Used with model versions Auraflow, Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Hunyuan Video, LTX2, Qwen, SD3, SD3 Large, Wan 2.1, Wan 2.1, Wan 2.2 5b, Z Image, Ernie Image and Cosmos2.5"""
    compression_artifacts_quality: float
    """compression_artifacts_quality Used with model versions Hunyuan Video, LTX2, Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
    tea_cache_end: int
    """tea_cache_end Used with model versions Flux.1, Hunyuan Video, Wan 2.1 and Wan 2.1"""
    cfg_zero_star: bool
    """cfg_zero_star Used with model versions Auraflow, Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Hunyuan Video, LTX2, Qwen, SD3, SD3 Large, Wan 2.1, Wan 2.1, Wan 2.2 5b, Z Image, Ernie Image and Cosmos2.5"""
    tea_cache: bool
    """tea_cache Used with model versions Flux.1, Hunyuan Video, Wan 2.1 and Wan 2.1"""
    causal_inference_pad: int
    """causal_inference_pad Used with model versions Wan 2.1, Wan 2.1 and Wan 2.2 5b"""


class Wan5bConfig(TypedDict, total=False):
    compression_artifacts: CompressionMethod
    """compression_artifacts Used with model versions Hunyuan Video, LTX2, Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
    causal_inference_enabled: bool
    """causal_inference_enabled Used with model versions Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
    num_frames: int
    """num_frames Used with model versions Hunyuan Video, LTX2, SVD, Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
    cfg_zero_init_steps: int
    """cfg_zero_init_steps Used with model versions Auraflow, Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Hunyuan Video, LTX2, Qwen, SD3, SD3 Large, Wan 2.1, Wan 2.1, Wan 2.2 5b, Z Image, Ernie Image and Cosmos2.5"""
    compression_artifacts_quality: float
    """compression_artifacts_quality Used with model versions Hunyuan Video, LTX2, Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
    cfg_zero_star: bool
    """cfg_zero_star Used with model versions Auraflow, Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Hunyuan Video, LTX2, Qwen, SD3, SD3 Large, Wan 2.1, Wan 2.1, Wan 2.2 5b, Z Image, Ernie Image and Cosmos2.5"""
    causal_inference: int
    """causal_inference Used with model versions Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
    causal_inference_pad: int
    """causal_inference_pad Used with model versions Wan 2.1, Wan 2.1 and Wan 2.2 5b"""


class TiledConfig(TypedDict, total=False):
    tiled_diffusion: bool
    """tiled_diffusion"""
    diffusion_tile_height: int
    """The height of each tile for tiled diffusion (will be rounded to the nearest 64)"""
    diffusion_tile_overlap: int
    """The overlap between tiles for tiled diffusion (will be rounded to the nearest 64)"""
    decoding_tile_width: int
    """The width of each tile for tiled decoding (will be rounded to the nearest 64)"""
    diffusion_tile_width: int
    """The width of each tile for tiled diffusion (will be rounded to the nearest 64)"""
    decoding_tile_height: int
    """The height of each tile for tiled decoding (will be rounded to the nearest 64)"""
    tiled_decoding: bool
    """tiled_decoding"""
    decoding_tile_overlap: int
    """The overlap between tiles for tiled decoding (will be rounded to the nearest 64)"""


class Flux2Config(TypedDict, total=False):
    speed_up_with_guidance_embed: bool
    """speed_up_with_guidance_embed Used with model versions Flux.1, Flux.2, HiDream and Hunyuan Video"""
    guidance_embed: float
    """guidance_embed Used with model versions Flux.1, Flux.2, HiDream and Hunyuan Video"""
    cfg_zero_init_steps: int
    """cfg_zero_init_steps Used with model versions Auraflow, Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Hunyuan Video, LTX2, Qwen, SD3, SD3 Large, Wan 2.1, Wan 2.1, Wan 2.2 5b, Z Image, Ernie Image and Cosmos2.5"""
    cfg_zero_star: bool
    """cfg_zero_star Used with model versions Auraflow, Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Hunyuan Video, LTX2, Qwen, SD3, SD3 Large, Wan 2.1, Wan 2.1, Wan 2.2 5b, Z Image, Ernie Image and Cosmos2.5"""
    resolution_dependent_shift: bool
    """resolution_dependent_shift Used with model versions Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Qwen, SD3, SD3 Large, Z Image and Cosmos2.5"""


class Flux2KleinConfig(TypedDict, total=False):
    cfg_zero_init_steps: int
    """cfg_zero_init_steps Used with model versions Auraflow, Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Hunyuan Video, LTX2, Qwen, SD3, SD3 Large, Wan 2.1, Wan 2.1, Wan 2.2 5b, Z Image, Ernie Image and Cosmos2.5"""
    cfg_zero_star: bool
    """cfg_zero_star Used with model versions Auraflow, Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Hunyuan Video, LTX2, Qwen, SD3, SD3 Large, Wan 2.1, Wan 2.1, Wan 2.2 5b, Z Image, Ernie Image and Cosmos2.5"""
    resolution_dependent_shift: bool
    """resolution_dependent_shift Used with model versions Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Qwen, SD3, SD3 Large, Z Image and Cosmos2.5"""


class QwenImageConfig(TypedDict, total=False):
    cfg_zero_init_steps: int
    """cfg_zero_init_steps Used with model versions Auraflow, Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Hunyuan Video, LTX2, Qwen, SD3, SD3 Large, Wan 2.1, Wan 2.1, Wan 2.2 5b, Z Image, Ernie Image and Cosmos2.5"""
    cfg_zero_star: bool
    """cfg_zero_star Used with model versions Auraflow, Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Hunyuan Video, LTX2, Qwen, SD3, SD3 Large, Wan 2.1, Wan 2.1, Wan 2.2 5b, Z Image, Ernie Image and Cosmos2.5"""
    resolution_dependent_shift: bool
    """resolution_dependent_shift Used with model versions Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Qwen, SD3, SD3 Large, Z Image and Cosmos2.5"""


class ZImageConfig(TypedDict, total=False):
    cfg_zero_init_steps: int
    """cfg_zero_init_steps Used with model versions Auraflow, Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Hunyuan Video, LTX2, Qwen, SD3, SD3 Large, Wan 2.1, Wan 2.1, Wan 2.2 5b, Z Image, Ernie Image and Cosmos2.5"""
    cfg_zero_star: bool
    """cfg_zero_star Used with model versions Auraflow, Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Hunyuan Video, LTX2, Qwen, SD3, SD3 Large, Wan 2.1, Wan 2.1, Wan 2.2 5b, Z Image, Ernie Image and Cosmos2.5"""
    resolution_dependent_shift: bool
    """resolution_dependent_shift Used with model versions Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Qwen, SD3, SD3 Large, Z Image and Cosmos2.5"""


class AnimaConfig(TypedDict, total=False):
    cfg_zero_init_steps: int
    """cfg_zero_init_steps Used with model versions Auraflow, Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Hunyuan Video, LTX2, Qwen, SD3, SD3 Large, Wan 2.1, Wan 2.1, Wan 2.2 5b, Z Image, Ernie Image and Cosmos2.5"""
    cfg_zero_star: bool
    """cfg_zero_star Used with model versions Auraflow, Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Hunyuan Video, LTX2, Qwen, SD3, SD3 Large, Wan 2.1, Wan 2.1, Wan 2.2 5b, Z Image, Ernie Image and Cosmos2.5"""
    resolution_dependent_shift: bool
    """resolution_dependent_shift Used with model versions Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Qwen, SD3, SD3 Large, Z Image and Cosmos2.5"""


class AuraFlowConfig(TypedDict, total=False):
    cfg_zero_init_steps: int
    """cfg_zero_init_steps Used with model versions Auraflow, Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Hunyuan Video, LTX2, Qwen, SD3, SD3 Large, Wan 2.1, Wan 2.1, Wan 2.2 5b, Z Image, Ernie Image and Cosmos2.5"""
    cfg_zero_star: bool
    """cfg_zero_star Used with model versions Auraflow, Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Hunyuan Video, LTX2, Qwen, SD3, SD3 Large, Wan 2.1, Wan 2.1, Wan 2.2 5b, Z Image, Ernie Image and Cosmos2.5"""


class ErnieImageConfig(TypedDict, total=False):
    cfg_zero_init_steps: int
    """cfg_zero_init_steps Used with model versions Auraflow, Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Hunyuan Video, LTX2, Qwen, SD3, SD3 Large, Wan 2.1, Wan 2.1, Wan 2.2 5b, Z Image, Ernie Image and Cosmos2.5"""
    cfg_zero_star: bool
    """cfg_zero_star Used with model versions Auraflow, Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Hunyuan Video, LTX2, Qwen, SD3, SD3 Large, Wan 2.1, Wan 2.1, Wan 2.2 5b, Z Image, Ernie Image and Cosmos2.5"""


c = CoreConfig()
x = ExtraConfig()
e = ErnieImageConfig()

f = c | x | e


class GenConfig(MutableMapping[str, object]):
    _d: dict[str, object]

    def __init__(self, **kwargs: object):
        self._d = dict(**kwargs)

    @override
    def __setitem__(self, key: str, value: object) -> None:
        self._d[key] = value

    @override
    def __delitem__(self, key: str) -> None:
        del self._d[key]

    @override
    def __iter__(self) -> Iterator[str]:
        return iter(self._d)

    @override
    def __len__(self) -> int:
        return len(self._d)

    @overload
    def __getitem__(
        self, name: Literal["seed", "width", "num_frames", "zero_cfg_init_steps"]
    ) -> int: ...
    @overload
    def __getitem__(
        self,
        name: Literal["strength", "guidance", "stochastic_sampling_gamma", "mask_blur"],
    ) -> float: ...
    @overload
    def __getitem__(self, name: Literal["model"]) -> str: ...
    @overload
    def __getitem__(self, name: str) -> object: ...

    @override
    def __getitem__(self, name: str) -> object:
        return self._d[name]


class CoreConfigC(GenConfig):
    def __init__(
        self,
        width: int | None = None,
        height: int | None = None,
        model: str | None = None,
    ):
        super().__init__(width=width, height=height, model=model)

    @override
    def __setitem__(self, key: str, value: object) -> None:
        self._d[key] = value

    @overload
    def __getitem__(self, name: Literal["seed", "width"]) -> int: ...
    @overload
    def __getitem__(self, name: Literal["strength", "guidance"]) -> float: ...
    @override
    def __getitem__(self, name: str) -> object:
        return self._d.get(name)


class FluxConfigC(GenConfig):
    def __init__(
        self,
        /,
        speed_up_with_guidance_embed: bool | None = None,
        tea_cache: bool | None = None,
    ):
        super().__init__(
            speed_up_with_guidance_embed=speed_up_with_guidance_embed,
            tea_cache=tea_cache,
        )

    @override
    def __setitem__(self, key: str, value: object) -> None:
        self._d[key] = value

    @overload
    def __getitem__(
        self, name: Literal["speed_up_with_guidance_embed", "tea_cache"]
    ) -> bool: ...
    @override
    def __getitem__(self, name: str) -> object:
        return self._d.get(name)


cc = CoreConfigC()

cc[""]

fc = FluxConfigC()

fc["tea_cache"] = 5
