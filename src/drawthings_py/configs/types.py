from typing import TypedDict
from enum import IntEnum, StrEnum

# ---------------------------------------------------------------------------
# Enums — accept int (from JSON) or name (for manual construction)
# Mirror the generated FlatBuffer enums but as proper Python IntEnums.
# ---------------------------------------------------------------------------


class SamplerType(IntEnum):
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

    @classmethod
    def from_fbs(cls, value: int) -> "SamplerType":
        return SamplerType(value)


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


class UpscalerModel(StrEnum):
    RealESRGANx2 = "realesrgan_x2plus_f16.ckpt"
    RealESRGANx4 = "realesrgan_x4plus_f16.ckpt"
    RealESRGANx4Anime = "realesrgan_x4plus_anime_6b_f16.ckpt"
    UniversalUpscaler = "esrgan_4x_universal_upscaler_v2_sharp_f16.ckpt"
    Remacri = "remacri_4x_f16.ckpt"
    UltraSharp = "4x_ultrasharp_f16.ckpt"


# ---------------------------------------------------------------------------
# Nested config types — field names match FlatBuffer schema (snake_cased)
# ---------------------------------------------------------------------------


class LoraDict(TypedDict, total=False):
    file: str
    weight: float
    mode: int | str  # LoRAMode enum


class ControlDict(TypedDict, total=False):
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
