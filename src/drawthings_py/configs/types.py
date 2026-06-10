from __future__ import annotations
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
    def from_value(cls, value: int | str) -> "SamplerType":
        if isinstance(value, int):
            return cls(value)
        return _SAMPLER_LOOKUP[value.lower()]


_SAMPLER_LOOKUP = {member.name.lower(): member for member in SamplerType}


class SeedMode(IntEnum):
    Legacy = 0
    TorchCpuCompatible = 1
    ScaleAlike = 2
    NvidiaGpuCompatible = 3

    @classmethod
    def from_value(cls, value: int | str) -> SeedMode:
        if isinstance(value, int):
            return cls(value)
        lookup = {
            "legacy": 0,
            "torchcpucompatible": 1,
            "scalealike": 2,
            "nvidiagpucompatible": 3,
        }
        return cls(lookup.get(value.lower().replace("_", ""), None))


class ControlMode(IntEnum):
    Balanced = 0
    Prompt = 1
    Control = 2

    @classmethod
    def from_value(cls, value: int | str) -> "ControlMode":
        if isinstance(value, int):
            return cls(value)
        lookup = {
            "balanced": 0,
            "prompt": 1,
            "control": 2,
        }
        return cls(lookup.get(value.lower().replace("_", ""), None))


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

    @classmethod
    def from_value(cls, value: int | str) -> "ControlInputType":
        if isinstance(value, int):
            return cls(value)
        lookup = {
            "unspecified": 0,
            "custom": 1,
            "depth": 2,
            "canny": 3,
            "scribble": 4,
            "pose": 5,
            "normalbae": 6,
            "color": 7,
            "lineart": 8,
            "softedge": 9,
            "seg": 10,
            "inpaint": 11,
            "ip2p": 12,
            "shuffle": 13,
            "mlsd": 14,
            "tile": 15,
            "blur": 16,
            "lowquality": 17,
            "gray": 18,
        }
        return cls(lookup.get(value.lower().replace("_", ""), None))


class LoraMode(IntEnum):
    All = 0
    Base = 1
    Refiner = 2

    @classmethod
    def from_value(cls, value: object) -> LoraMode:
        if isinstance(value, int):
            return cls(value)
        if isinstance(value, str):
            lookup = {
                "all": 0,
                "base": 1,
                "refiner": 2,
            }
            return cls(lookup.get(value.lower().replace("_", ""), cls.All))
        return cls.All


class CompressionMethod(IntEnum):
    Disabled = 0
    H264 = 1
    H265 = 2
    Jpeg = 3

    @classmethod
    def from_value(cls, value: int | str) -> "CompressionMethod":
        if isinstance(value, int):
            return cls(value)
        lookup = {
            "disabled": 0,
            "h264": 1,
            "h265": 2,
            "jpeg": 3,
        }
        return cls(lookup.get(value.lower().replace("_", ""), None))


class UpscalerModel(StrEnum):
    RealESRGANx2 = "realesrgan_x2plus_f16.ckpt"
    RealESRGANx4 = "realesrgan_x4plus_f16.ckpt"
    RealESRGANx4Anime = "realesrgan_x4plus_anime_6b_f16.ckpt"
    UniversalUpscaler = "esrgan_4x_universal_upscaler_v2_sharp_f16.ckpt"
    Remacri = "remacri_4x_f16.ckpt"
    UltraSharp = "4x_ultrasharp_f16.ckpt"

    @classmethod
    def from_value(cls, value: str) -> UpscalerModel | None:
        try:
            return cls(value)
        except ValueError:
            return None


# ---------------------------------------------------------------------------
# Nested config types — field names match FlatBuffer schema (snake_cased)
# ---------------------------------------------------------------------------


class LoraDict(TypedDict, total=False):
    file: str
    weight: float
    mode: LoraMode


class LoraList(list[LoraDict]):
    pass


class ControlDict(TypedDict, total=False):
    file: str
    weight: float
    guidanceStart: float
    guidanceEnd: float
    noPrompt: bool
    globalAveragePooling: bool
    downSamplingRate: float
    controlMode: int | str  # ControlMode enum
    targetBlocks: list[str]
    inputOverride: int | str  # ControlInputType enum
