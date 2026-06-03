"""
Builds a FlatBuffer GenerationConfiguration from a Config TypedDict.
Intentionally does very little validation
"""

from __future__ import annotations
from typing import Any
from enum import IntEnum

import flatbuffers

from .generated.dt_grpc import Control as FBControl
from .generated.dt_grpc import GenerationConfiguration as GenConfig
from .generated.dt_grpc import LoRA as FBLoRA
from .configs.types import (
    CompressionMethod,
    ConfigDict,
    Control,
    ControlInputType,
    ControlMode,
    Lora,
    LoRAMode,
    Sampler,
    SeedMode,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _resolve_enum(value: int | str, enum_cls: type[IntEnum]) -> int:
    """Resolve an enum value from an int ordinal or a string member name."""
    if isinstance(value, int):
        return int(enum_cls(value))
    if isinstance(value, str):
        for member in enum_cls:
            if member.name.lower() == value.lower():
                return int(member)
        valid = ", ".join(m.name for m in enum_cls)
        raise ValueError(
            f"Unknown {enum_cls.__name__} value: {value!r}. Valid names: {valid}"
        )
    raise TypeError(
        f"Expected int or str for {enum_cls.__name__}, got {type(value).__name__}"
    )


def _div64(value: int) -> int:
    """Convert a pixel dimension to FlatBuffer tile units (÷64)."""
    return value // 64


# ---------------------------------------------------------------------------
# Nested table builders (must be called *before* the parent table starts)
# ---------------------------------------------------------------------------


def _build_lora(builder: flatbuffers.Builder, lora: Lora) -> int:
    """Serialize a single LoRA table. Returns the FlatBuffer offset."""
    file_off = builder.CreateString(lora["file"]) if "file" in lora else None

    FBLoRA.Start(builder)
    if file_off is not None:
        FBLoRA.AddFile(builder, file_off)
    if "weight" in lora:
        FBLoRA.AddWeight(builder, lora["weight"])
    if "mode" in lora:
        FBLoRA.AddMode(builder, _resolve_enum(lora["mode"], LoRAMode))
    return FBLoRA.End(builder)


def _build_control(builder: flatbuffers.Builder, control: Control) -> int:
    """Serialize a single Control table. Returns the FlatBuffer offset."""
    file_off = builder.CreateString(control["file"]) if "file" in control else None

    # target_blocks string vector
    tb_off = None
    if "target_blocks" in control and control["target_blocks"]:
        block_offsets = [builder.CreateString(b) for b in control["target_blocks"]]
        FBControl.StartTargetBlocksVector(builder, len(block_offsets))
        for off in reversed(block_offsets):
            builder.PrependUOffsetTRelative(off)
        tb_off = builder.EndVector()

    FBControl.Start(builder)
    if file_off is not None:
        FBControl.AddFile(builder, file_off)
    if "weight" in control:
        FBControl.AddWeight(builder, control["weight"])
    if "guidance_start" in control:
        FBControl.AddGuidanceStart(builder, control["guidance_start"])
    if "guidance_end" in control:
        FBControl.AddGuidanceEnd(builder, control["guidance_end"])
    if "no_prompt" in control:
        FBControl.AddNoPrompt(builder, control["no_prompt"])
    if "global_average_pooling" in control:
        FBControl.AddGlobalAveragePooling(builder, control["global_average_pooling"])
    if "down_sampling_rate" in control:
        FBControl.AddDownSamplingRate(builder, control["down_sampling_rate"])
    if "control_mode" in control:
        FBControl.AddControlMode(
            builder, _resolve_enum(control["control_mode"], ControlMode)
        )
    if tb_off is not None:
        FBControl.AddTargetBlocks(builder, tb_off)
    if "input_override" in control:
        FBControl.AddInputOverride(
            builder, _resolve_enum(control["input_override"], ControlInputType)
        )
    return FBControl.End(builder)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def build_configuration(config: ConfigDict, builder_size: int = 1024) -> bytes:
    """
    Build a FlatBuffer ``GenerationConfiguration`` from a :class:`Config` dict.

    All height / width / overlap fields are specified in **pixels** and are
    automatically divided by 64 for the FlatBuffer wire format.

    Enum fields (``sampler``, ``seed_mode``, ``compression_artifacts``, etc.)
    accept either an ``int`` ordinal or a case-insensitive ``str`` member name.

    Returns the finished FlatBuffer as ``bytes``.
    """
    builder = flatbuffers.Builder(builder_size)

    # ------------------------------------------------------------------
    # Phase 1: pre-create strings & nested tables (must precede StartObject)
    # ------------------------------------------------------------------
    def _str(key: str) -> int | None:
        v = config.get(key)
        if v == "":
            v = None
        return builder.CreateString(v) if v is not None else None

    model_off = _str("model")
    refiner_model_off = _str("refiner_model")
    upscaler_off = _str("upscaler")
    face_restoration_off = _str("face_restoration")
    name_off = _str("name")
    clip_l_text_off = _str("clip_l_text")
    open_clip_g_text_off = _str("open_clip_g_text")
    t5_text_off = _str("t5_text")

    # Nested tables — build in reverse order for correct FlatBuffer layout
    lora_offsets = []
    for lora in reversed(config.get("loras", [])):
        lora_offsets.append(_build_lora(builder, lora))
    lora_offsets.reverse()

    control_offsets = []
    for ctrl in reversed(config.get("controls", [])):
        control_offsets.append(_build_control(builder, ctrl))
    control_offsets.reverse()

    # Vectors of nested tables
    loras_vec = None
    if lora_offsets:
        GenConfig.StartLorasVector(builder, len(lora_offsets))
        for off in reversed(lora_offsets):
            builder.PrependUOffsetTRelative(off)
        loras_vec = builder.EndVector()

    controls_vec = None
    if control_offsets:
        GenConfig.StartControlsVector(builder, len(control_offsets))
        for off in reversed(control_offsets):
            builder.PrependUOffsetTRelative(off)
        controls_vec = builder.EndVector()

    # ------------------------------------------------------------------
    # Phase 2: build the GenerationConfiguration table
    # ------------------------------------------------------------------
    GenConfig.Start(builder)

    def _get(key: str, default: Any = None):
        return config.get(key, default)

    # --- scalars: direct name matches -----------------------------------
    if (v := _get("seed")) is not None:
        GenConfig.AddSeed(builder, v)

    if (v := _get("id")) is not None:
        GenConfig.AddId(builder, v)

    if (v := _get("steps")) is not None:
        GenConfig.AddSteps(builder, v)
    if (v := _get("guidance_scale")) is not None:
        GenConfig.AddGuidanceScale(builder, v)
    if (v := _get("strength")) is not None:
        GenConfig.AddStrength(builder, v)
    if (v := _get("image_guidance_scale")) is not None:
        GenConfig.AddImageGuidanceScale(builder, v)
    if (v := _get("batch_count")) is not None:
        GenConfig.AddBatchCount(builder, v)
    if (v := _get("batch_size")) is not None:
        GenConfig.AddBatchSize(builder, v)
    if (v := _get("clip_skip")) is not None:
        GenConfig.AddClipSkip(builder, v)
    if (v := _get("mask_blur")) is not None:
        GenConfig.AddMaskBlur(builder, v)
    if (v := _get("mask_blur_outset")) is not None:
        GenConfig.AddMaskBlurOutset(builder, v)
    if (v := _get("sharpness")) is not None:
        GenConfig.AddSharpness(builder, v)
    if (v := _get("shift")) is not None:
        GenConfig.AddShift(builder, v)
    if (v := _get("stochastic_sampling_gamma")) is not None:
        GenConfig.AddStochasticSamplingGamma(builder, v)
    if (v := _get("refiner_start")) is not None:
        GenConfig.AddRefinerStart(builder, v)
    if (v := _get("upscaler_scale_factor")) is not None:
        GenConfig.AddUpscalerScaleFactor(builder, v)
    if (v := _get("num_frames")) is not None:
        GenConfig.AddNumFrames(builder, v)
    if (v := _get("guidance_embed")) is not None:
        GenConfig.AddGuidanceEmbed(builder, v)
    if (v := _get("clip_weight")) is not None:
        GenConfig.AddClipWeight(builder, v)
    if (v := _get("image_prior_steps")) is not None:
        GenConfig.AddImagePriorSteps(builder, v)
    if (v := _get("aesthetic_score")) is not None:
        GenConfig.AddAestheticScore(builder, v)
    if (v := _get("negative_aesthetic_score")) is not None:
        GenConfig.AddNegativeAestheticScore(builder, v)
    if (v := _get("stage_2_steps")) is not None:
        GenConfig.AddStage2Steps(builder, v)
    if (v := _get("stage_2_shift")) is not None:
        GenConfig.AddStage2Shift(builder, v)
    if (v := _get("tea_cache_start")) is not None:
        GenConfig.AddTeaCacheStart(builder, v)
    if (v := _get("tea_cache_end")) is not None:
        GenConfig.AddTeaCacheEnd(builder, v)
    if (v := _get("tea_cache_threshold")) is not None:
        GenConfig.AddTeaCacheThreshold(builder, v)
    if (v := _get("tea_cache_max_skip_steps")) is not None:
        GenConfig.AddTeaCacheMaxSkipSteps(builder, v)
    if (v := _get("causal_inference")) is not None:
        GenConfig.AddCausalInference(builder, v)
        # Derive causal_inference_enabled from the value
        GenConfig.AddCausalInferenceEnabled(builder, v > 0)
    if (v := _get("causal_inference_pad")) is not None:
        GenConfig.AddCausalInferencePad(builder, v)
    if (v := _get("cfg_zero_init_steps")) is not None:
        GenConfig.AddCfgZeroInitSteps(builder, v)
    if (v := _get("compression_artifacts_quality")) is not None:
        GenConfig.AddCompressionArtifactsQuality(builder, v)
    if (v := _get("hires_fix_strength")) is not None:
        GenConfig.AddHiresFixStrength(builder, v)

    # --- booleans -------------------------------------------------------

    if (v := _get("hires_fix")) is not None:
        GenConfig.AddHiresFix(builder, v)
    if (v := _get("tiled_decoding")) is not None:
        GenConfig.AddTiledDecoding(builder, v)
    if (v := _get("tiled_diffusion")) is not None:
        GenConfig.AddTiledDiffusion(builder, v)
    if (v := _get("separate_clip_l")) is not None:
        GenConfig.AddSeparateClipL(builder, v)
    if (v := _get("separate_open_clip_g")) is not None:
        GenConfig.AddSeparateOpenClipG(builder, v)
    if (v := _get("speed_up_with_guidance_embed")) is not None:
        GenConfig.AddSpeedUpWithGuidanceEmbed(builder, v)
    if (v := _get("resolution_dependent_shift")) is not None:
        GenConfig.AddResolutionDependentShift(builder, v)
    if (v := _get("tea_cache")) is not None:
        GenConfig.AddTeaCache(builder, v)
    if (v := _get("t5_text_encoder")) is not None:
        GenConfig.AddT5TextEncoder(builder, v)
    if (v := _get("separate_t5")) is not None:
        GenConfig.AddSeparateT5(builder, v)
    if (v := _get("preserve_original_after_inpaint")) is not None:
        GenConfig.AddPreserveOriginalAfterInpaint(builder, v)
    if (v := _get("negative_prompt_for_image_prior")) is not None:
        GenConfig.AddNegativePromptForImagePrior(builder, v)
    if (v := _get("zero_negative_prompt")) is not None:
        GenConfig.AddZeroNegativePrompt(builder, v)
    if (v := _get("cfg_zero_star")) is not None:
        GenConfig.AddCfgZeroStar(builder, v)

    # --- enums ----------------------------------------------------------

    if (v := _get("sampler")) is not None:
        GenConfig.AddSampler(builder, _resolve_enum(v, Sampler))
    if (v := _get("seed_mode")) is not None:
        GenConfig.AddSeedMode(builder, _resolve_enum(v, SeedMode))
    # CHANGE FROM DEFAULT FBS TO MATCH DT
    else:
        GenConfig.AddSeedMode(builder, SeedMode.ScaleAlike)
    if (v := _get("compression_artifacts")) is not None:
        GenConfig.AddCompressionArtifacts(builder, _resolve_enum(v, CompressionMethod))

    # --- renamed fields -------------------------------------------------

    if (v := _get("fps")) is not None:
        GenConfig.AddFpsId(builder, v)
    if (v := _get("motion_scale")) is not None:
        GenConfig.AddMotionBucketId(builder, v)
    if (v := _get("guiding_frame_noise")) is not None:
        GenConfig.AddCondAug(builder, v)
    if (v := _get("start_frame_guidance")) is not None:
        GenConfig.AddStartFrameCfg(builder, v)
    if (v := _get("stage_2_guidance")) is not None:
        GenConfig.AddStage2Cfg(builder, v)

    # --- pixel → ÷64 fields --------------------------------------------

    if (v := _get("width")) is not None:
        GenConfig.AddStartWidth(builder, _div64(v))
    if (v := _get("height")) is not None:
        GenConfig.AddStartHeight(builder, _div64(v))

    # these need to have a fallback value
    # these should use 512
    GenConfig.AddHiresFixStartWidth(builder, _div64(_get("hires_fix_width", 512)))
    GenConfig.AddHiresFixStartHeight(builder, _div64(_get("hires_fix_height", 512)))

    # these should use 1024 for width/height and 128 for overlap
    GenConfig.AddDecodingTileWidth(builder, _div64(_get("decoding_tile_width", 1024)))
    GenConfig.AddDecodingTileHeight(builder, _div64(_get("decoding_tile_height", 1024)))
    GenConfig.AddDecodingTileOverlap(
        builder, _div64(_get("decoding_tile_overlap", 128))
    )
    GenConfig.AddDiffusionTileWidth(builder, _div64(_get("diffusion_tile_width", 1024)))
    GenConfig.AddDiffusionTileHeight(
        builder, _div64(_get("diffusion_tile_height", 1024))
    )
    GenConfig.AddDiffusionTileOverlap(
        builder, _div64(_get("diffusion_tile_overlap", 128))
    )

    # these should use the start_width and start_height as fallback values
    GenConfig.AddOriginalImageHeight(
        builder, _div64(_get("original_image_height", _get("height", 512)))
    )
    GenConfig.AddOriginalImageWidth(
        builder, _div64(_get("original_image_width", _get("width", 512)))
    )
    GenConfig.AddTargetImageHeight(
        builder, _div64(_get("target_image_height", _get("height", 512)))
    )
    GenConfig.AddTargetImageWidth(
        builder, _div64(_get("target_image_width", _get("width", 512)))
    )
    GenConfig.AddNegativeOriginalImageHeight(
        builder, _div64(_get("negative_original_image_height", _get("height", 512)))
    )
    GenConfig.AddNegativeOriginalImageWidth(
        builder, _div64(_get("negative_original_image_width", _get("width", 512)))
    )

    # --- strings (pre-created offsets) ----------------------------------

    if model_off is not None:
        GenConfig.AddModel(builder, model_off)
    if refiner_model_off is not None:
        GenConfig.AddRefinerModel(builder, refiner_model_off)
    if upscaler_off is not None:
        GenConfig.AddUpscaler(builder, upscaler_off)
    if face_restoration_off is not None:
        GenConfig.AddFaceRestoration(builder, face_restoration_off)
    if name_off is not None:
        GenConfig.AddName(builder, name_off)
    if clip_l_text_off is not None:
        GenConfig.AddClipLText(builder, clip_l_text_off)
    if open_clip_g_text_off is not None:
        GenConfig.AddOpenClipGText(builder, open_clip_g_text_off)
    if t5_text_off is not None:
        GenConfig.AddT5Text(builder, t5_text_off)

    # --- nested table vectors -------------------------------------------

    if controls_vec is not None:
        GenConfig.AddControls(builder, controls_vec)
    if loras_vec is not None:
        GenConfig.AddLoras(builder, loras_vec)

    # ------------------------------------------------------------------
    # Finish
    # ------------------------------------------------------------------
    root = GenConfig.End(builder)
    builder.Finish(root)
    return bytes(builder.Output())
