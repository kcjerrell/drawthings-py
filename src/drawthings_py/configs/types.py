from __future__ import annotations
from enum import StrEnum
import json
from typing import TypedDict, cast
from .enums import (
    CompressionMethod,
    ControlMode,
    ControlInputType,
    LoraMode,
    SamplerType,
    SeedMode,
    control_input_type_from_value,
    control_mode_from_value,
)


from drawthings_py._util import ensure_str


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


class LoraDict(TypedDict, total=False):
    file: str
    weight: float
    mode: LoraMode


class ControlDict(TypedDict, total=False):
    file: str
    weight: float
    guidanceStart: float
    guidanceEnd: float
    noPrompt: bool
    globalAveragePooling: bool
    downSamplingRate: float
    controlMode: ControlMode
    targetBlocks: list[str]
    inputOverride: ControlInputType


def control_dict_from_json(data: object) -> ControlDict | None:
    if isinstance(data, str):
        d = cast(dict[str, object], json.loads(data))
    elif isinstance(data, dict):
        d = cast(dict[str, object], data)
    else:
        return None
    file = ensure_str(d.get("file"))
    if not file:
        return None

    return ControlDict(
        {
            "file": file,
            "weight": float(cast(str | float | int | None, d.get("weight")) or 1.0),
            "guidanceStart": float(
                cast(str | float | int | None, d.get("guidanceStart")) or 0.0
            ),
            "guidanceEnd": float(
                cast(str | float | int | None, d.get("guidanceEnd")) or 1.0
            ),
            "noPrompt": bool(d.get("noPrompt", False)),
            "globalAveragePooling": bool(d.get("globalAveragePooling", True)),
            "downSamplingRate": float(
                cast(str | float | int | None, d.get("downSamplingRate")) or 1.0
            ),
            "controlMode": control_mode_from_value(d.get("controlMode")),
            "targetBlocks": cast(list[str] | None, d.get("targetBlocks")) or [],
            "inputOverride": control_input_type_from_value(d.get("inputOverride")),
        }
    )


__all__ = [
    "CompressionMethod",
    "ControlMode",
    "ControlInputType",
    "LoraMode",
    "SamplerType",
    "SeedMode",
    "UpscalerModel",
    "LoraDict",
    "ControlDict",
    "control_dict_from_json",
]
