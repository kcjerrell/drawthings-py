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


from drawthings_py.util._util import ensure_str, get_keys_value, instead


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
    guidance_start: float
    guidance_end: float
    no_prompt: bool
    global_average_pooling: bool
    down_sampling_rate: float
    control_mode: ControlMode
    target_blocks: list[str]
    input_override: ControlInputType


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
            "guidance_start": float(
                cast(
                    str | float | int | None,
                    get_keys_value(d, "guidance_start", "guidanceStart"),
                )
                or 0.0
            ),
            "guidance_end": float(
                cast(
                    str | float | int | None,
                    get_keys_value(d, "guidance_end", "guidanceEnd"),
                )
                or 1.0
            ),
            "no_prompt": bool(get_keys_value(d, "no_prompt", "noPrompt")),
            # unless explicitly false, global_average_pooling should be true
            "global_average_pooling": bool(
                instead(
                    get_keys_value(d, "global_average_pooling", "globalAveragePooling"),
                    True,
                )
            ),
            "down_sampling_rate": float(
                cast(
                    str | float | int | None,
                    get_keys_value(d, "down_sampling_rate", "downSamplingRate"),
                )
                or 1.0
            ),
            "control_mode": control_mode_from_value(
                get_keys_value(d, "control_mode", "controlMode")
            ),
            "target_blocks": cast(
                list[str] | None, get_keys_value(d, "target_blocks", "targetBlocks")
            )
            or [],
            "input_override": control_input_type_from_value(
                get_keys_value(d, "input_override", "inputOverride")
            ),
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
