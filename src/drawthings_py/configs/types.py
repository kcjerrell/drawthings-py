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
    """Supported upscaler models available in Draw Things."""

    RealESRGANx2 = "realesrgan_x2plus_f16.ckpt"
    RealESRGANx4 = "realesrgan_x4plus_f16.ckpt"
    RealESRGANx4Anime = "realesrgan_x4plus_anime_6b_f16.ckpt"
    UniversalUpscaler = "esrgan_4x_universal_upscaler_v2_sharp_f16.ckpt"
    Remacri = "remacri_4x_f16.ckpt"
    UltraSharp = "4x_ultrasharp_f16.ckpt"

    @classmethod
    def from_value(cls, value: str) -> UpscalerModel | None:
        """Parse an UpscalerModel from a string value.

        Args:
            value: The string representation of the model file name.

        Returns:
            UpscalerModel | None: The matched UpscalerModel, or None if not found.
        """
        try:
            return cls(value)
        except ValueError:
            return None


class LoraDict(TypedDict, total=False):
    """Dictionary representation of a LoRA configuration."""

    file: str
    """The file path or identifier of the LoRA model."""
    weight: float
    """The default influence weight of the LoRA model."""
    mode: LoraMode
    """The target components mode (All, Base, Refiner) for the LoRA."""


class ControlDict(TypedDict, total=False):
    """Dictionary representation of a ControlNet configuration."""

    file: str
    """The file path or identifier of the ControlNet model."""
    weight: float
    """The influence weight of the ControlNet model."""
    guidance_start: float
    """The step index (percentage) where ControlNet guidance starts."""
    guidance_end: float
    """The step index (percentage) where ControlNet guidance ends."""
    no_prompt: bool
    """Whether to disable prompt influence for this ControlNet."""
    global_average_pooling: bool
    """Whether to apply global average pooling to the ControlNet features."""
    down_sampling_rate: float
    """The downsampling rate applied to control image features."""
    control_mode: ControlMode
    """The control mode balance (Balanced, Prompt, Control)."""
    target_blocks: list[str]
    """Specific neural network target block names to apply control on."""
    input_override: ControlInputType
    """The input type override category (e.g. Canny, Depth)."""


def control_dict_from_json(data: object) -> ControlDict | None:
    """Parse a ControlDict from a JSON string or dictionary.

    Args:
        data: The input JSON string or dictionary object.

    Returns:
        ControlDict | None: The parsed ControlDict, or None if invalid or missing the 'file' key.
    """
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
