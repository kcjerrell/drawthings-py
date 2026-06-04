from typing import TypedDict
from enum import IntEnum

# ---------------------------------------------------------------------------
# Enums — accept int (from JSON) or name (for manual construction)
# Mirror the generated FlatBuffer enums but as proper Python IntEnums.
# ---------------------------------------------------------------------------


class Sampler(IntEnum):
    DPMPP2MKarras = 0
    EulerA = 1
    DDIM = 2
    PLMS = 3
    DPMPPSDEKarras = 4
    UniPC = 5
    LCM = 6
    EulerASubstep = 7
    DPMPPSDESubstep = 8
    TCD = 9
    EulerATrailing = 10
    DPMPPSDETrailing = 11
    DPMPP2MAYS = 12
    EulerAAYS = 13
    DPMPPSDEAYS = 14
    DPMPP2MTrailing = 15
    DDIMTrailing = 16
    UniPCTrailing = 17
    UniPCAYS = 18
    TCDTrailing = 19


class SeedMode(IntEnum):
    Legacy = 0
    TorchCpuCompatible = 1
    ScaleAlike = 2
    NvidiaGpuCompatible = 3


class ControlMode(IntEnum):
    Balanced = 0
    Prompt = 1
    Control = 2


class ControlInputType(IntEnum):
    Unspecified = 0
    Custom = 1
    Depth = 2
    Canny = 3
    Scribble = 4
    Pose = 5
    Normalbae = 6
    Color = 7
    Lineart = 8
    Softedge = 9
    Seg = 10
    Inpaint = 11
    Ip2p = 12
    Shuffle = 13
    Mlsd = 14
    Tile = 15
    Blur = 16
    Lowquality = 17
    Gray = 18


class LoRAMode(IntEnum):
    All = 0
    Base = 1
    Refiner = 2


class CompressionMethod(IntEnum):
    Disabled = 0
    H264 = 1
    H265 = 2
    Jpeg = 3


# ---------------------------------------------------------------------------
# Nested config types — field names match FlatBuffer schema (snake_cased)
# ---------------------------------------------------------------------------


class Lora(TypedDict, total=False):
    file: str
    weight: float
    mode: int | str  # LoRAMode enum


class Control(TypedDict, total=False):
    file: str
    weight: float
    guidance_start: float
    guidance_end: float
    no_prompt: bool
    global_average_pooling: bool
    down_sampling_rate: float
    control_mode: int | str  # ControlMode enum
    target_blocks: list[str]
    input_override: int | str  # ControlInputType enum


# ---------------------------------------------------------------------------
# Top-level generation configuration
#
# Field names match the Draw Things app JSON config (snake_cased).
# All height/width dimensions are specified in **pixels**; they are
# automatically converted to tile units (÷64) when building the FlatBuffer.
# ---------------------------------------------------------------------------


class ConfigDict(TypedDict, total=False):
    id: int

    # core generation
    width: int
    height: int
    seed: int
    seed_mode: int | str  # SeedMode enum
    steps: int
    guidance_scale: float
    strength: float
    sampler: int | str  # Sampler enum
    batch_count: int
    batch_size: int
    clip_skip: int
    mask_blur: float
    mask_blur_outset: int
    sharpness: float
    shift: float
    image_guidance_scale: float
    stochastic_sampling_gamma: float

    # model references
    model: str
    refiner_model: str
    refiner_start: float
    upscaler: str
    upscaler_scale_factor: int

    # controls & loras
    controls: list[Control]
    loras: list[Lora]

    # hires fix
    hires_fix: bool
    hires_fix_width: int
    hires_fix_height: int
    hires_fix_strength: float

    # tiled decoding
    tiled_decoding: bool
    decoding_tile_width: int
    decoding_tile_height: int
    decoding_tile_overlap: int

    # tiled diffusion
    tiled_diffusion: bool
    diffusion_tile_width: int
    diffusion_tile_height: int
    diffusion_tile_overlap: int

    # clip text overrides
    separate_clip_l: bool
    clip_l_text: str
    separate_open_clip_g: bool
    open_clip_g_text: str

    # guidance embed
    speed_up_with_guidance_embed: bool
    guidance_embed: float

    # resolution dependent shift
    resolution_dependent_shift: bool

    # tea cache
    tea_cache: bool
    tea_cache_start: int
    tea_cache_end: int
    tea_cache_threshold: float
    tea_cache_max_skip_steps: int

    # t5
    t5_text_encoder: bool
    separate_t5: bool
    t5_text: str

    # video / animation
    num_frames: int
    fps: int
    motion_scale: int
    guiding_frame_noise: float
    start_frame_guidance: float

    # causal inference
    causal_inference: int
    causal_inference_pad: int

    # inpainting
    preserve_original_after_inpaint: bool

    # face restoration
    face_restoration: str

    # SDXL-specific
    original_image_height: int
    original_image_width: int
    crop_top: int
    crop_left: int
    target_image_height: int
    target_image_width: int
    negative_original_image_height: int
    negative_original_image_width: int

    # aesthetic
    aesthetic_score: float
    negative_aesthetic_score: float
    zero_negative_prompt: bool

    # Kandinsky
    clip_weight: float
    negative_prompt_for_image_prior: bool
    image_prior_steps: int

    # stage 2
    stage_2_steps: int
    stage_2_guidance: float
    stage_2_shift: float

    # cfg zero
    cfg_zero_star: bool
    cfg_zero_init_steps: int

    # compression
    compression_artifacts: int | str  # CompressionMethod enum
    compression_artifacts_quality: float

    # misc
    name: str
