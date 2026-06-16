from enum import StrEnum
from importlib.resources import files
import json
from typing import Literal, Required, TypedDict, cast

from .config_dict import ConfigDict

PresetName = Literal[
    "qwen_image_2512_lightning",
    "flux_1_fill_dev",
    "anima_preview_3",
    "flux_1_schnell",
    "flux_1_dev",
    "flux_2_klein_4b_base",
    "ernie_image_base",
    "z_image_turbo",
    "sdxl",
    "qwen_image_2512",
    "stable_diffusion",
    "flux_2_klein_9b",
    "flux_2_dev_with_turbo",
    "flux_2_klein_9b_kv",
    "qwen_image_edit_2511",
    "qwen_image_edit_2511_lightning",
    "z_image_base",
    "flux_2_klein_4b",
    "ernie_image_turbo",
    "flux_2_klein_9b_base",
    "chroma_hd",
]


class Presets(StrEnum):
    qwen_image_2512_lightning = "qwen_image_2512_lightning"
    flux_1_fill_dev = "flux_1_fill_dev"
    anima_preview_3 = "anima_preview_3"
    flux_1_schnell = "flux_1_schnell"
    flux_1_dev = "flux_1_dev"
    flux_2_klein_4b_base = "flux_2_klein_4b_base"
    ernie_image_base = "ernie_image_base"
    z_image_turbo = "z_image_turbo"
    sdxl = "sdxl"
    qwen_image_2512 = "qwen_image_2512"
    stable_diffusion = "stable_diffusion"
    flux_2_klein_9b = "flux_2_klein_9b"
    flux_2_dev_with_turbo = "flux_2_dev_with_turbo"
    flux_2_klein_9b_kv = "flux_2_klein_9b_kv"
    qwen_image_edit_2511 = "qwen_image_edit_2511"
    qwen_image_edit_2511_lightning = "qwen_image_edit_2511_lightning"
    z_image_base = "z_image_base"
    flux_2_klein_4b = "flux_2_klein_4b"
    ernie_image_turbo = "ernie_image_turbo"
    flux_2_klein_9b_base = "flux_2_klein_9b_base"
    chroma_hd = "chroma_hd"


class PresetDefinition(TypedDict, total=False):
    configuration: Required[ConfigDict]
    name: Required[str]
    version: str

def load_preset_data(name: PresetName | Presets | str) -> PresetDefinition:
    """Get the JSON string for a named preset.

    Args:
        name: The name of the preset to get.

    Returns:
        A JSON string containing the preset data.
    """
    filename = name + ".json"
    path = files("drawthings_py.resources.configs") / filename
    preset: PresetDefinition | None = None
    with path.open("r", encoding="utf-8") as f:
        preset = cast(PresetDefinition | None, json.load(f))
    if preset is None:
        raise ValueError(f"Unknown preset: {name}")
    return preset


def load_preset_config(name: PresetName | Presets) -> str:
    """Get the JSON string for a named preset.

    Args:
        name: The name of the preset to get.

    Returns:
        A JSON string containing the preset data.
    """
    return json.dumps(load_preset_data(name)["configuration"])