from enum import StrEnum
from typing import Literal, Required, TypedDict

from drawthings_py.configs.gen_config_generated import ConfigDict

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
