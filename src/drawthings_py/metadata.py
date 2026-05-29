from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
import sys
import struct
from typing import Any

from .generated.dt_grpc.GenerationConfiguration import GenerationConfiguration

SAMPLER_NAMES = {
    0: "DPM++ 2M Karras",
    1: "Euler A",
    2: "DDIM",
    3: "PLMS",
    4: "DPM++ SDE Karras",
    5: "UniPC",
    6: "LCM",
    7: "Euler A Substep",
    8: "DPM++ SDE Substep",
    9: "TCD",
    10: "Euler A Trailing",
    11: "DPM++ SDE Trailing",
    12: "DPM++ 2M AYS",
    13: "Euler A AYS",
    14: "DPM++ SDE AYS",
    15: "DPM++ 2M Trailing",
    16: "DDIM Trailing",
    17: "UniPC Trailing",
    18: "UniPC AYS",
    19: "TCD Trailing",
}

SEED_MODE_NAMES = {
    0: "Legacy",
    1: "Torch CPU Compatible",
    2: "Scale Alike",
    3: "Nvidia GPU Compatible",
}

COMPRESSION_ARTIFACT_NAMES = {
    0: "disabled",
    1: "h264",
    2: "h265",
    3: "jpeg",
}

LORA_MODE_NAMES = {
    0: "all",
    1: "base",
    2: "refiner",
}

CONTROL_MODE_NAMES = {
    0: "balanced",
    1: "prompt",
    2: "control",
}

CONTROL_INPUT_TYPE_NAMES = {
    0: "unspecified",
    1: "custom",
    2: "depth",
    3: "canny",
    4: "scribble",
    5: "pose",
    6: "normalbae",
    7: "color",
    8: "lineart",
    9: "softedge",
    10: "seg",
    11: "inpaint",
    12: "ip2p",
    13: "shuffle",
    14: "mlsd",
    15: "tile",
    16: "blur",
    17: "lowquality",
    18: "gray",
}


FIELD_SLOTS = {
    "Id": 0,
    "StartWidth": 1,
    "StartHeight": 2,
    "Seed": 3,
    "Steps": 4,
    "GuidanceScale": 5,
    "Strength": 6,
    "Model": 7,
    "Sampler": 8,
    "BatchCount": 9,
    "BatchSize": 10,
    "HiresFix": 11,
    "HiresFixStartWidth": 12,
    "HiresFixStartHeight": 13,
    "HiresFixStrength": 14,
    "Upscaler": 15,
    "ImageGuidanceScale": 16,
    "SeedMode": 17,
    "ClipSkip": 18,
    "Controls": 19,
    "Loras": 20,
    "MaskBlur": 21,
    "FaceRestoration": 22,
    "ClipWeight": 25,
    "NegativePromptForImagePrior": 26,
    "ImagePriorSteps": 27,
    "RefinerModel": 28,
    "OriginalImageHeight": 29,
    "OriginalImageWidth": 30,
    "CropTop": 31,
    "CropLeft": 32,
    "TargetImageHeight": 33,
    "TargetImageWidth": 34,
    "AestheticScore": 35,
    "NegativeAestheticScore": 36,
    "ZeroNegativePrompt": 37,
    "RefinerStart": 38,
    "NegativeOriginalImageHeight": 39,
    "NegativeOriginalImageWidth": 40,
    "Name": 41,
    "FpsId": 42,
    "MotionBucketId": 43,
    "CondAug": 44,
    "StartFrameCfg": 45,
    "NumFrames": 46,
    "MaskBlurOutset": 47,
    "Sharpness": 48,
    "Shift": 49,
    "Stage2Steps": 50,
    "Stage2Cfg": 51,
    "Stage2Shift": 52,
    "TiledDecoding": 53,
    "DecodingTileWidth": 54,
    "DecodingTileHeight": 55,
    "DecodingTileOverlap": 56,
    "StochasticSamplingGamma": 57,
    "PreserveOriginalAfterInpaint": 58,
    "TiledDiffusion": 59,
    "DiffusionTileWidth": 60,
    "DiffusionTileHeight": 61,
    "DiffusionTileOverlap": 62,
    "UpscalerScaleFactor": 63,
    "T5TextEncoder": 64,
    "SeparateClipL": 65,
    "ClipLText": 66,
    "SeparateOpenClipG": 67,
    "OpenClipGText": 68,
    "SpeedUpWithGuidanceEmbed": 69,
    "GuidanceEmbed": 70,
    "ResolutionDependentShift": 71,
    "TeaCacheStart": 72,
    "TeaCacheEnd": 73,
    "TeaCacheThreshold": 74,
    "TeaCache": 75,
    "SeparateT5": 76,
    "T5Text": 77,
    "TeaCacheMaxSkipSteps": 78,
    "CausalInferenceEnabled": 79,
    "CausalInference": 80,
    "CausalInferencePad": 81,
    "CfgZeroStar": 82,
    "CfgZeroInitSteps": 83,
    "CompressionArtifacts": 84,
    "CompressionArtifactsQuality": 85,
}

APP_DEFAULTS = {
    "clipLText": "Abstract patterns and colors, unfinished, raw",
    "hiresFixHeight": 960,
    "hiresFixWidth": 960,
    "causalInference": 0,
    "guidanceEmbed": 4.5,
    "numFrames": 81,
    "refinerStart": 0.23,
    "teaCacheThreshold": 0.2,
}


def create_metadata(config: GenerationConfiguration, prompt: str, negative_prompt: str) -> dict:
    """Create Draw Things PNG metadata from the generation configuration."""
    cfg = config
    width = _pixels(cfg.StartWidth())
    height = _pixels(cfg.StartHeight())
    model = _decode_string(cfg.Model()) or ""
    sampler = cfg.Sampler()
    seed_mode = cfg.SeedMode()
    v2 = _create_v2_metadata(cfg, width, height, model, sampler, seed_mode)

    return {
        "c": prompt or "",
        "mask_blur": cfg.MaskBlur(),
        "model": model,
        "sampler": SAMPLER_NAMES.get(sampler, str(sampler)),
        "scale": 1,
        "seed": cfg.Seed(),
        "seed_mode": SEED_MODE_NAMES.get(seed_mode, str(seed_mode)),
        "shift": cfg.Shift(),
        "size": f"{width}x{height}",
        "steps": cfg.Steps(),
        "stochastic_sampling_gamma": _float32(cfg.StochasticSamplingGamma()),
        "strength": cfg.Strength(),
        "uc": negative_prompt or "",
        "v2": v2,
    }


def _create_v2_metadata(
    cfg: GenerationConfiguration,
    width: int,
    height: int,
    model: str,
    sampler: int,
    seed_mode: int,
) -> dict[str, Any]:
    return {
        "aestheticScore": _value(cfg, "AestheticScore"),
        "batchCount": _value(cfg, "BatchCount"),
        "batchSize": _value(cfg, "BatchSize"),
        "causalInference": _value(
            cfg, "CausalInference", APP_DEFAULTS["causalInference"]
        ),
        "causalInferencePad": _value(cfg, "CausalInferencePad"),
        "cfgZeroInitSteps": _value(cfg, "CfgZeroInitSteps"),
        "cfgZeroStar": _value(cfg, "CfgZeroStar"),
        "clipLText": _string_value(cfg, "ClipLText", APP_DEFAULTS["clipLText"]),
        "clipSkip": _value(cfg, "ClipSkip"),
        "clipWeight": _value(cfg, "ClipWeight"),
        "compressionArtifacts": COMPRESSION_ARTIFACT_NAMES.get(
            _value(cfg, "CompressionArtifacts"),
            str(_value(cfg, "CompressionArtifacts")),
        ),
        "compressionArtifactsQuality": _value(cfg, "CompressionArtifactsQuality"),
        "controls": _controls(cfg),
        "cropLeft": _value(cfg, "CropLeft"),
        "cropTop": _value(cfg, "CropTop"),
        "decodingTileHeight": _pixels(_value(cfg, "DecodingTileHeight")),
        "decodingTileOverlap": _pixels(_value(cfg, "DecodingTileOverlap")),
        "decodingTileWidth": _pixels(_value(cfg, "DecodingTileWidth")),
        "diffusionTileHeight": _pixels(_value(cfg, "DiffusionTileHeight")),
        "diffusionTileOverlap": _pixels(_value(cfg, "DiffusionTileOverlap")),
        "diffusionTileWidth": _pixels(_value(cfg, "DiffusionTileWidth")),
        "fps": _value(cfg, "FpsId"),
        "guidanceEmbed": _value(cfg, "GuidanceEmbed", APP_DEFAULTS["guidanceEmbed"]),
        "guidanceScale": _value(cfg, "GuidanceScale"),
        "guidingFrameNoise": _value(cfg, "CondAug"),
        "height": height,
        "hiresFix": _value(cfg, "HiresFix"),
        "hiresFixHeight": _pixels_value(
            cfg, "HiresFixStartHeight", APP_DEFAULTS["hiresFixHeight"]
        ),
        "hiresFixStrength": _value(cfg, "HiresFixStrength"),
        "hiresFixWidth": _pixels_value(
            cfg, "HiresFixStartWidth", APP_DEFAULTS["hiresFixWidth"]
        ),
        "id": _value(cfg, "Id"),
        "imageGuidanceScale": _value(cfg, "ImageGuidanceScale"),
        "imagePriorSteps": _value(cfg, "ImagePriorSteps"),
        "loras": _loras(cfg),
        "maskBlur": _value(cfg, "MaskBlur"),
        "maskBlurOutset": _value(cfg, "MaskBlurOutset"),
        "model": model,
        "motionScale": _value(cfg, "MotionBucketId"),
        "negativeAestheticScore": _value(cfg, "NegativeAestheticScore"),
        "negativeOriginalImageHeight": _pixels_value(
            cfg, "NegativeOriginalImageHeight", 512
        ),
        "negativeOriginalImageWidth": _pixels_value(
            cfg, "NegativeOriginalImageWidth", 512
        ),
        "negativePromptForImagePrior": _value(cfg, "NegativePromptForImagePrior"),
        "numFrames": _value(cfg, "NumFrames", APP_DEFAULTS["numFrames"]),
        "originalImageHeight": _pixels_value(cfg, "OriginalImageHeight", height),
        "originalImageWidth": _pixels_value(cfg, "OriginalImageWidth", width),
        "preserveOriginalAfterInpaint": _value(cfg, "PreserveOriginalAfterInpaint"),
        "refinerStart": _value(cfg, "RefinerStart", APP_DEFAULTS["refinerStart"]),
        "resolutionDependentShift": _value(cfg, "ResolutionDependentShift"),
        "sampler": sampler,
        "seed": _value(cfg, "Seed"),
        "seedMode": seed_mode,
        "separateClipL": _value(cfg, "SeparateClipL"),
        "separateOpenClipG": _value(cfg, "SeparateOpenClipG"),
        "separateT5": _value(cfg, "SeparateT5"),
        "sharpness": _value(cfg, "Sharpness"),
        "shift": _metadata_float(_value(cfg, "Shift")),
        "speedUpWithGuidanceEmbed": _value(cfg, "SpeedUpWithGuidanceEmbed"),
        "stage2Guidance": _value(cfg, "Stage2Cfg"),
        "stage2Shift": _value(cfg, "Stage2Shift"),
        "stage2Steps": _value(cfg, "Stage2Steps"),
        "startFrameGuidance": _value(cfg, "StartFrameCfg"),
        "steps": _value(cfg, "Steps"),
        "stochasticSamplingGamma": _metadata_float(
            _value(cfg, "StochasticSamplingGamma")
        ),
        "strength": _value(cfg, "Strength"),
        "t5TextEncoder": _value(cfg, "T5TextEncoder"),
        "targetImageHeight": _pixels_value(cfg, "TargetImageHeight", height),
        "targetImageWidth": _pixels_value(cfg, "TargetImageWidth", width),
        "teaCache": _value(cfg, "TeaCache"),
        "teaCacheEnd": _value(cfg, "TeaCacheEnd"),
        "teaCacheMaxSkipSteps": _value(cfg, "TeaCacheMaxSkipSteps"),
        "teaCacheStart": _value(cfg, "TeaCacheStart"),
        "teaCacheThreshold": _value(
            cfg, "TeaCacheThreshold", APP_DEFAULTS["teaCacheThreshold"]
        ),
        "tiledDecoding": _value(cfg, "TiledDecoding"),
        "tiledDiffusion": _value(cfg, "TiledDiffusion"),
        "upscalerScaleFactor": _value(cfg, "UpscalerScaleFactor"),
        "width": width,
        "zeroNegativePrompt": _value(cfg, "ZeroNegativePrompt"),
    }


def _value(
    cfg: GenerationConfiguration,
    name: str,
    metadata_default: Any | None = None,
) -> Any:
    if metadata_default is not None and not _field_present(cfg, name):
        return metadata_default
    return getattr(cfg, name)()


def _pixels_value(
    cfg: GenerationConfiguration,
    name: str,
    metadata_default: int,
) -> int:
    if not _field_present(cfg, name):
        return metadata_default
    value = _pixels(getattr(cfg, name)())
    return value or metadata_default


def _field_present(cfg: GenerationConfiguration, name: str) -> bool:
    return cfg._tab.Offset(4 + (FIELD_SLOTS[name] * 2)) != 0


def _decode_string(value: bytes | None) -> str | None:
    if value is None:
        return None
    return value.decode("utf-8")


def _string_value(
    cfg: GenerationConfiguration,
    name: str,
    metadata_default: str,
) -> str:
    if not _field_present(cfg, name):
        return metadata_default
    return _decode_string(getattr(cfg, name)()) or ""


def _pixels(value: int) -> int:
    return int(value) * 64


def _float32(value: float) -> float:
    return struct.unpack("f", struct.pack("f", float(value)))[0]


def _metadata_float(value: float) -> float:
    return round(float(value), 7)


def _loras(cfg: GenerationConfiguration) -> list[dict[str, Any]]:
    return [
        {
            "mode": LORA_MODE_NAMES.get(lora.Mode(), str(lora.Mode())),
            "file": _decode_string(lora.File()) or "",
            "weight": lora.Weight(),
        }
        for lora in _nested_items(cfg, "Loras", "LorasLength")
    ]


def _controls(cfg: GenerationConfiguration) -> list[dict[str, Any]]:
    controls = []
    for control in _nested_items(cfg, "Controls", "ControlsLength"):
        controls.append(
            {
                "file": _decode_string(control.File()) or "",
                "weight": control.Weight(),
                "guidanceStart": control.GuidanceStart(),
                "guidanceEnd": control.GuidanceEnd(),
                "noPrompt": control.NoPrompt(),
                "globalAveragePooling": control.GlobalAveragePooling(),
                "downSamplingRate": control.DownSamplingRate(),
                "controlMode": CONTROL_MODE_NAMES.get(
                    control.ControlMode(), str(control.ControlMode())
                ),
                "targetBlocks": [
                    _decode_string(control.TargetBlocks(index)) or ""
                    for index in range(control.TargetBlocksLength())
                ],
                "inputOverride": CONTROL_INPUT_TYPE_NAMES.get(
                    control.InputOverride(), str(control.InputOverride())
                ),
            }
        )
    return controls


def _nested_items(
    cfg: GenerationConfiguration,
    item_name: str,
    length_name: str,
) -> list[Any]:
    generated_dir = str(Path(__file__).parent / "generated" / "dt_grpc")
    added_path = generated_dir not in sys.path
    if added_path:
        sys.path.append(generated_dir)
    try:
        item: Callable[[int], Any] = getattr(cfg, item_name)
        length: Callable[[], int] = getattr(cfg, length_name)
        return [item(index) for index in range(length())]
    finally:
        if added_path:
            sys.path.remove(generated_dir)

def _with_seed(metadata: dict, seed: int) -> dict:
    new_metadata = metadata.copy()
    new_metadata["v2"] = metadata["v2"].copy()
    new_metadata["seed"] = seed
    new_metadata["v2"]["seed"] = seed
    return new_metadata