from __future__ import annotations

import copy
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any, Required, TypedDict, cast

from drawthings_py.generated.dt_grpc.config_generated import GenerationConfiguration

SAMPLER_NAMES: dict[Any, str] = {
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


class V2(TypedDict, total=False):
    aestheticScore: float
    batchCount: int
    batchSize: int
    causalInference: bool
    causalInferencePad: int
    cfgZeroInitSteps: int
    cfgZeroStar: float
    clipLText: float
    clipSkip: int
    clipWeight: float
    compressionArtifacts: str
    compressionArtifactsQuality: int
    controls: list[dict[str, Any]]
    cropLeft: int
    cropTop: int
    decodingTileHeight: int
    decodingTileOverlap: int
    decodingTileWidth: int
    diffusionTileHeight: int
    diffusionTileOverlap: int
    diffusionTileWidth: int
    fps: int
    guidanceEmbed: bool
    guidanceScale: float
    height: int
    hiresFix: bool
    hiresFixHeight: int
    hiresFixStrength: float
    hiresFixWidth: int
    id: int
    imageGuidanceScale: float
    imagePriorSteps: int
    loras: list[dict[str, Any]]
    maskBlur: float
    maskBlurOutset: int
    motionScale: int
    negativeAestheticScore: float
    seed: int
    steps: int
    width: int


class ImageMetadata(TypedDict, total=False):
    c: str
    uc: str
    steps: Required[int]
    sampler: Required[str]
    scale: Required[float]
    seed: Required[int]
    size: Required[str]
    model: Required[str]
    strength: Required[float]
    seed_mode: Required[str]
    shift: Required[float]
    v2: Required[V2]


def create_metadata(
    config: GenerationConfiguration, prompt: str, negative_prompt: str
) -> ImageMetadata:
    """Create Draw Things PNG metadata from the generation configuration."""
    cfg = config
    width = _pixels(cfg.StartWidth())
    height = _pixels(cfg.StartHeight())
    model = _decode_string(cfg.Model()) or ""
    sampler = cfg.Sampler()
    seed_mode = cfg.SeedMode()
    v2 = _create_v2_metadata(cfg, width, height, model, sampler, seed_mode)

    return ImageMetadata(
        c=prompt or "",
        uc=negative_prompt or "",
        model=model,
        sampler=SAMPLER_NAMES.get(sampler, str(sampler)),
        scale=cfg.GuidanceScale(),
        seed=cfg.Seed(),
        seed_mode=SEED_MODE_NAMES.get(seed_mode, str(seed_mode)),
        shift=cfg.Shift(),
        size=f"{width}x{height}",
        steps=cfg.Steps(),
        strength=cfg.Strength(),
        v2=v2,
    )


def _create_v2_metadata(
    cfg: GenerationConfiguration,
    width: int,
    height: int,
    model: str,
    sampler: int,
    seed_mode: int,
) -> V2:
    v2: dict[str, Any] = {
        "aestheticScore": cfg.AestheticScore(),
        "batchCount": cfg.BatchCount(),
        "batchSize": cfg.BatchSize(),
        "causalInference": cfg.CausalInference(),
        "causalInferencePad": cfg.CausalInferencePad(),
        "cfgZeroInitSteps": cfg.CfgZeroInitSteps(),
        "cfgZeroStar": cfg.CfgZeroStar(),
        "clipLText": cfg.ClipLText(),
        "clipSkip": cfg.ClipSkip(),
        "clipWeight": cfg.ClipWeight(),
        "compressionArtifacts": COMPRESSION_ARTIFACT_NAMES.get(
            cfg.CompressionArtifacts(),
        ),
        "compressionArtifactsQuality": cfg.CompressionArtifactsQuality(),
        "controls": _controls(cfg),
        "cropLeft": cfg.CropLeft(),
        "cropTop": cfg.CropTop(),
        "decodingTileHeight": _pixels(cfg.DecodingTileHeight()),
        "decodingTileOverlap": _pixels(cfg.DecodingTileOverlap()),
        "decodingTileWidth": _pixels(cfg.DecodingTileWidth()),
        "diffusionTileHeight": _pixels(cfg.DiffusionTileHeight()),
        "diffusionTileOverlap": _pixels(cfg.DiffusionTileOverlap()),
        "diffusionTileWidth": _pixels(cfg.DiffusionTileWidth()),
        "fps": cfg.FpsId(),
        "guidanceEmbed": cfg.GuidanceEmbed(),
        "guidanceScale": cfg.GuidanceScale(),
        "guidingFrameNoise": cfg.CondAug(),
        "height": height,
        "hiresFix": cfg.HiresFix(),
        "hiresFixHeight": _pixels(cfg.HiresFixStartHeight()),
        "hiresFixStrength": cfg.HiresFixStrength(),
        "hiresFixWidth": _pixels(cfg.HiresFixStartWidth()),
        "id": cfg.Id(),
        "imageGuidanceScale": cfg.ImageGuidanceScale(),
        "imagePriorSteps": cfg.ImagePriorSteps(),
        "loras": _loras(cfg),
        "maskBlur": cfg.MaskBlur(),
        "maskBlurOutset": cfg.MaskBlurOutset(),
        "model": model,
        "motionScale": cfg.MotionBucketId(),
        "negativeAestheticScore": cfg.NegativeAestheticScore(),
        "negativeOriginalImageHeight": _pixels(cfg.NegativeOriginalImageHeight()),
        "negativeOriginalImageWidth": _pixels(cfg.NegativeOriginalImageWidth()),
        "negativePromptForImagePrior": cfg.NegativePromptForImagePrior(),
        "numFrames": cfg.NumFrames(),
        "originalImageHeight": _pixels(cfg.OriginalImageHeight()),
        "originalImageWidth": _pixels(cfg.OriginalImageWidth()),
        "preserveOriginalAfterInpaint": cfg.PreserveOriginalAfterInpaint(),
        "refinerStart": cfg.RefinerStart(),
        "resolutionDependentShift": cfg.ResolutionDependentShift(),
        "sampler": sampler,
        "seed": cfg.Seed(),
        "seedMode": seed_mode,
        "separateClipL": cfg.SeparateClipL(),
        "separateOpenClipG": cfg.SeparateOpenClipG(),
        "separateT5": cfg.SeparateT5(),
        "sharpness": cfg.Sharpness(),
        "shift": _metadata_float(cfg.Shift()),
        "speedUpWithGuidanceEmbed": cfg.SpeedUpWithGuidanceEmbed(),
        "stage2Guidance": cfg.Stage2Cfg(),
        "stage2Shift": cfg.Stage2Shift(),
        "stage2Steps": cfg.Stage2Steps(),
        "startFrameGuidance": cfg.StartFrameCfg(),
        "steps": cfg.Steps(),
        "stochasticSamplingGamma": _metadata_float(cfg.StochasticSamplingGamma()),
        "strength": cfg.Strength(),
        "t5TextEncoder": cfg.T5TextEncoder(),
        "targetImageHeight": _pixels(cfg.TargetImageHeight()),
        "targetImageWidth": _pixels(cfg.TargetImageWidth()),
        "teaCache": cfg.TeaCache(),
        "teaCacheEnd": cfg.TeaCacheEnd(),
        "teaCacheMaxSkipSteps": cfg.TeaCacheMaxSkipSteps(),
        "teaCacheStart": cfg.TeaCacheStart(),
        "teaCacheThreshold": cfg.TeaCacheThreshold(),
        "tiledDecoding": cfg.TiledDecoding(),
        "tiledDiffusion": cfg.TiledDiffusion(),
        "upscalerScaleFactor": cfg.UpscalerScaleFactor(),
        "width": width,
        "zeroNegativePrompt": cfg.ZeroNegativePrompt(),
    }
    v2 = {k: v for k, v in v2.items() if v is not None and v != ""}
    return cast(V2, v2)  # pyright: ignore[reportInvalidCast]


def _decode_string(value: bytes | str | None) -> str | None:
    if value is None:
        return None
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return value


def _pixels(value: int | None) -> int:
    return (value or 0) * 64


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


def copy_with_seed(metadata: ImageMetadata, seed: int) -> ImageMetadata:
    new_metadata = copy.deepcopy(metadata)
    new_metadata["seed"] = seed
    new_metadata["v2"]["seed"] = seed
    return new_metadata
