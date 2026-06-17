from typing import TypeGuard, TypedDict, TypeAlias, Literal, get_args
from drawthings_py.configs.types import (
    CompressionMethod,
    ControlDict,
    LoraDict,
    SamplerType,
    SeedMode,
    UpscalerModel,
)

ConfigValue: TypeAlias = (
    bool
    | CompressionMethod
    | float
    | int
    | list[ControlDict]
    | list[LoraDict]
    | SamplerType
    | SeedMode
    | str
    | UpscalerModel
    | None
)

ConfigKey = Literal[
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
    "controls",
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

_CONFIG_KEYS = frozenset(get_args(ConfigKey))


def is_config_key(value: str) -> TypeGuard[ConfigKey]:
    return value in _CONFIG_KEYS


class ConfigDict(TypedDict, total=False):
    id: int
    """Unused. id"""
    width: int
    """Width of the image in pixels (will be rounded to the nearest 64)"""
    height: int
    """Height of the image in pixels (will be rounded to the nearest 64)"""
    seed: int
    """controls the random number generation for the diffusion process, enabling reproducible image outputs when the same seed is used with identical parameters"""
    steps: int
    """specifies the number of sampling iterations (denoising steps) performed during the image generation process"""
    guidance: float
    """controls how strongly the generation follows the text prompt (also called CFG or text guidance)"""
    strength: float
    """determines the denoising strength for img2img operations"""
    model: str | None
    """specifies which model file to use for generation"""
    sampler: SamplerType
    """specifies the sampling algorithm and schedule to use for generation"""
    loras: list[LoraDict]
    """array of LoRA objects specifying LoRA models to apply during image generation"""
    controls: list[ControlDict]
    """array of control objects specifying control models to apply during image generation"""
    batch_count: int
    """Unused. batch_count"""
    batch_size: int
    """number of images to generate in a single batch"""
    hires_fix: bool
    """enables high-resolution fix for generation. When enabled, image generation begins at a lower resoution, then switches to the full size at the specified point"""
    hires_fix_width: int
    """width to use for the first-pass generation"""
    hires_fix_height: int
    """height to use for the first-pass generation"""
    hires_fix_strength: float
    """What percentage of steps are used in the full size generation"""
    upscaler: UpscalerModel | None
    """specifies which upscaler model to use for generation"""
    image_guidance_scale: float
    """used with HiDream E-1 to determine how strongly the init image is followed. Used with model version HiDream"""
    seed_mode: SeedMode
    """specifies how seeds are used for batch generation"""
    clip_skip: int
    """determines how many layers of the CLIP model to skip during processing. Used with model versions SD, SD2, SDXL and SDXL"""
    mask_blur: float
    """specifies the degree of blurring applied to masks for inpainting or image manipulations"""
    face_restoration: str | None
    """indicates the model to be used for enhancing faces in generated images"""
    decode_with_attention: bool
    """Unused. decode_with_attention"""
    hires_fix_decode_with_attention: bool
    """Unused. hires_fix_decode_with_attention"""
    clip_weight: float
    """Unused. clip_weight"""
    negative_prompt_for_image_prior: bool
    """Unused. negative_prompt_for_image_prior"""
    image_prior_steps: int
    """Unused. image_prior_steps"""
    refiner_model: str | None
    """specifies the name or identifier of a refiner model to enhance image quality"""
    original_image_height: int
    """The original height before image cropped during training (will be rounded to the nearest 64). Used with model versions SDXL and SDXL"""
    original_image_width: int
    """The original width before image cropped during training (will be rounded to the nearest 64). Used with model versions SDXL and SDXL"""
    crop_top: int
    """The top crop offset before image cropped during training (will be rounded to the nearest 64). Used with model versions SDXL and SDXL"""
    crop_left: int
    """The left crop offset before image cropped during training (will be rounded to the nearest 64). Used with model versions SDXL and SDXL"""
    target_image_height: int
    """The target height after image cropped during training (will be rounded to the nearest 64). Used with model versions SDXL and SDXL"""
    target_image_width: int
    """The target width after image cropped during training (will be rounded to the nearest 64). Used with model versions SDXL and SDXL"""
    aesthetic_score: float
    """Unused. aesthetic_score"""
    negative_aesthetic_score: float
    """Unused. negative_aesthetic_score"""
    zero_negative_prompt: bool
    """when true, treats the negative prompt as empty during generation. Used with model versions Flux.1, HiDream, Pixart, SD3, SD3 Large, SDXL, SDXL and SSD"""
    refiner_start: float
    """determines at what point (percentage of steps) the refiner model should begin working"""
    negative_original_image_height: int
    """The negative original image height (will be rounded to the nearest 64). Used with model versions SDXL and SDXL"""
    negative_original_image_width: int
    """The negative original image width (will be rounded to the nearest 64). Used with model versions SDXL and SDXL"""
    name: str | None
    """Unused. name"""
    fps: int
    """specifies the frames per second for video generation. Used with model version SVD"""
    motion_scale: int
    """controls the intensity or scale of motion in generated videos. Used with model version SVD"""
    guiding_frame_noise: float
    """controls the amount of noise added to the guiding frame during video generation. Used with model version SVD"""
    guiding_frame_guidance: float
    """determines the guidance strength for the starting frame during video generation. Used with model version SVD"""
    num_frames: int
    """specifies the total number of frames to generate for a video. Used with model versions Hunyuan Video, LTX2, SVD, Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
    mask_blur_outset: int
    """controls the outward expansion and blurring of a mask used during image generation"""
    sharpness: float
    """influences the overall sharpness of the generated image"""
    shift: float
    """applies a general transformation or offset during image generation"""
    stage_2_steps: int
    """Unused. stage_2_steps"""
    stage_2_cfg: float
    """Unused. stage_2_cfg"""
    stage_2_shift: float
    """Unused. stage_2_shift"""
    tiled_decoding: bool
    """enables memory optimization technique for decoding images in smaller tiles"""
    decoding_tile_width: int
    """The width of each tile for tiled decoding (will be rounded to the nearest 64)"""
    decoding_tile_height: int
    """The height of each tile for tiled decoding (will be rounded to the nearest 64)"""
    decoding_tile_overlap: int
    """The overlap between tiles for tiled decoding (will be rounded to the nearest 64)"""
    stochastic_sampling_gamma: float
    """controls the Strategic Stochastic Sampling feature for TCD/TCDTrailing samplers"""
    preserve_original_after_inpaint: bool
    """determines whether the original image content is preserved after inpainting"""
    tiled_diffusion: bool
    """enables a tiled approach for the diffusion process during image generation"""
    diffusion_tile_width: int
    """The width of each tile for tiled diffusion (will be rounded to the nearest 64)"""
    diffusion_tile_height: int
    """The height of each tile for tiled diffusion (will be rounded to the nearest 64)"""
    diffusion_tile_overlap: int
    """The overlap between tiles for tiled diffusion (will be rounded to the nearest 64)"""
    upscaler_scale_factor: int
    """specifies the scaling factor to be applied by an upscaler"""
    t5_text_encoder: bool
    """indicates whether a T5 text encoder should be used during image generation. Used with model versions SD3 and SD3 Large"""
    separate_clip_l: bool
    """indicates that a separate text prompt should be used for the CLIP L text encoder. Used with model versions Flux.1, HiDream, SD3 and SD3 Large"""
    clip_l_text: str | None
    """holds the specific text prompt to be used when separate_clip_l is enabled. Used with model versions Flux.1, HiDream, SD3 and SD3 Large"""
    separate_open_clip_g: bool
    """enables the use of a distinct text prompt for the OpenCLIP G text encoder. Used with model versions HiDream, SD3 and SD3 Large"""
    open_clip_g_text: str | None
    """stores custom text for the OpenCLIP-G text encoder when separate_open_clip_g is enabled. Used with model versions HiDream, SD3 and SD3 Large"""
    speed_up_with_guidance_embed: bool
    """enables an optimization technique using pre-computed guidance embeddings. Used with model versions Flux.1, Flux.2, HiDream and Hunyuan Video"""
    guidance_embed: float
    """controls the strength of the guidance embedding when speed_up_with_guidance_embed is active. Used with model versions Flux.1, Flux.2, HiDream and Hunyuan Video"""
    resolution_dependent_shift: bool
    """controls whether shift adjustments should be resolution-dependent during image generation. Used with model versions Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Qwen, SD3, SD3 Large, Z Image and Cosmos2.5"""
    tea_cache_start: int
    """specifies the starting step index for TeaCache acceleration. Used with model versions Flux.1, Hunyuan Video, Wan 2.1 and Wan 2.1"""
    tea_cache_end: int
    """specifies the ending step index for TeaCache acceleration. Used with model versions Flux.1, Hunyuan Video, Wan 2.1 and Wan 2.1"""
    tea_cache_threshold: float
    """threshold for determining whether a diffusion sampling step can be skipped. Used with model versions Flux.1, Hunyuan Video, Wan 2.1 and Wan 2.1"""
    tea_cache: bool
    """enables or disables the TeaCache acceleration mechanism. Used with model versions Flux.1, Hunyuan Video, Wan 2.1 and Wan 2.1"""
    separate_t5: bool
    """controls whether the T5 text encoder is processed separately from other text encoders. Used with model version HiDream"""
    t5_text: str | None
    """stores custom text for a separate T5 text encoder when separate_t5 is enabled. Used with model version HiDream"""
    tea_cache_max_skip_steps: int
    """controls the maximum number of steps that can be skipped when using TeaCache acceleration. Used with model versions Flux.1, Hunyuan Video, Wan 2.1 and Wan 2.1"""
    causal_inference_enabled: bool
    """toggle for causal inference optimization. Used with model versions Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
    causal_inference: int
    """enables a causal inference optimization technique when set to a value greater than 0. Used with model versions Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
    causal_inference_pad: int
    """specifies padding for the causal inference operation. Used with model versions Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
    cfg_zero_star: bool
    """enables the CFG Zero* technique, an advanced guidance method. Used with model versions Auraflow, Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Hunyuan Video, LTX2, Qwen, SD3, SD3 Large, Wan 2.1, Wan 2.1, Wan 2.2 5b, Z Image, Ernie Image and Cosmos2.5"""
    cfg_zero_init_steps: int
    """specifies the number of initial steps to use with CFG zero initialization. Used with model versions Auraflow, Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Hunyuan Video, LTX2, Qwen, SD3, SD3 Large, Wan 2.1, Wan 2.1, Wan 2.2 5b, Z Image, Ernie Image and Cosmos2.5"""
    compression_artifacts: CompressionMethod
    """determines which compression method to apply to generated artifacts. Used with model versions Hunyuan Video, LTX2, Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
    compression_artifacts_quality: float
    """controls the quality level of compression when a compression method is enabled. Used with model versions Hunyuan Video, LTX2, Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
