import flatbuffers
from typing import Any

from .types import (
    ConfigDict,
    ControlDict,
    LoraDict,
    SamplerType,
    SeedMode,
    ControlMode,
    ControlInputType,
    LoRAMode,
    CompressionMethod,
)
from drawthings_py.generated.dt_grpc.config_generated import (  # type: ignore
    GenerationConfigurationStart,
    GenerationConfigurationEnd,
    GenerationConfigurationAddStartWidth,
    GenerationConfigurationAddStartHeight,
    GenerationConfigurationAddSeed,
    GenerationConfigurationAddSteps,
    GenerationConfigurationAddGuidanceScale,
    GenerationConfigurationAddImageGuidanceScale,
    GenerationConfigurationAddStrength,
    GenerationConfigurationAddModel,
    GenerationConfigurationAddSampler,
    GenerationConfigurationAddBatchSize,
    GenerationConfigurationAddHiresFix,
    GenerationConfigurationAddHiresFixStartWidth,
    GenerationConfigurationAddHiresFixStartHeight,
    GenerationConfigurationAddHiresFixStrength,
    GenerationConfigurationAddUpscaler,
    GenerationConfigurationAddSeedMode,
    GenerationConfigurationAddClipSkip,
    GenerationConfigurationAddControls,
    GenerationConfigurationStartControlsVector,
    GenerationConfigurationAddLoras,
    GenerationConfigurationStartLorasVector,
    GenerationConfigurationAddMaskBlur,
    GenerationConfigurationAddFaceRestoration,
    GenerationConfigurationAddNegativePromptForImagePrior,
    GenerationConfigurationAddRefinerModel,
    GenerationConfigurationAddOriginalImageHeight,
    GenerationConfigurationAddOriginalImageWidth,
    GenerationConfigurationAddCropTop,
    GenerationConfigurationAddCropLeft,
    GenerationConfigurationAddTargetImageHeight,
    GenerationConfigurationAddTargetImageWidth,
    GenerationConfigurationAddAestheticScore,
    GenerationConfigurationAddNegativeAestheticScore,
    GenerationConfigurationAddZeroNegativePrompt,
    GenerationConfigurationAddRefinerStart,
    GenerationConfigurationAddNegativeOriginalImageHeight,
    GenerationConfigurationAddNegativeOriginalImageWidth,
    GenerationConfigurationAddName,
    GenerationConfigurationAddFpsId,
    GenerationConfigurationAddMotionBucketId,
    GenerationConfigurationAddCondAug,
    GenerationConfigurationAddStartFrameCfg,
    GenerationConfigurationAddNumFrames,
    GenerationConfigurationAddMaskBlurOutset,
    GenerationConfigurationAddSharpness,
    GenerationConfigurationAddShift,
    GenerationConfigurationAddTiledDecoding,
    GenerationConfigurationAddDecodingTileWidth,
    GenerationConfigurationAddDecodingTileHeight,
    GenerationConfigurationAddDecodingTileOverlap,
    GenerationConfigurationAddStochasticSamplingGamma,
    GenerationConfigurationAddPreserveOriginalAfterInpaint,
    GenerationConfigurationAddTiledDiffusion,
    GenerationConfigurationAddDiffusionTileWidth,
    GenerationConfigurationAddDiffusionTileHeight,
    GenerationConfigurationAddDiffusionTileOverlap,
    GenerationConfigurationAddUpscalerScaleFactor,
    GenerationConfigurationAddT5TextEncoder,
    GenerationConfigurationAddSeparateClipL,
    GenerationConfigurationAddClipLText,
    GenerationConfigurationAddSeparateOpenClipG,
    GenerationConfigurationAddOpenClipGText,
    GenerationConfigurationAddSpeedUpWithGuidanceEmbed,
    GenerationConfigurationAddGuidanceEmbed,
    GenerationConfigurationAddResolutionDependentShift,
    GenerationConfigurationAddTeaCacheStart,
    GenerationConfigurationAddTeaCacheEnd,
    GenerationConfigurationAddTeaCacheThreshold,
    GenerationConfigurationAddTeaCache,
    GenerationConfigurationAddSeparateT5,
    GenerationConfigurationAddT5Text,
    GenerationConfigurationAddTeaCacheMaxSkipSteps,
    GenerationConfigurationAddCausalInferenceEnabled,
    GenerationConfigurationAddCausalInference,
    GenerationConfigurationAddCausalInferencePad,
    GenerationConfigurationAddCfgZeroStar,
    GenerationConfigurationAddCfgZeroInitSteps,
    GenerationConfigurationAddCompressionArtifacts,
    GenerationConfigurationAddCompressionArtifactsQuality,
    ControlStart,
    ControlEnd,
    ControlAddFile,
    ControlAddWeight,
    ControlAddGuidanceStart,
    ControlAddGuidanceEnd,
    ControlAddNoPrompt,
    ControlAddGlobalAveragePooling,
    ControlAddDownSamplingRate,
    ControlAddControlMode,
    ControlAddTargetBlocks,
    ControlStartTargetBlocksVector,
    ControlAddInputOverride,
    LoRAStart,
    LoRAEnd,
    LoRAAddFile,
    LoRAAddWeight,
    LoRAAddMode,
)


def _to_enum_value(value: Any, enum_class: type) -> int:  # type: ignore
    """Convert enum value (int, str, or enum) to integer value."""
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        return getattr(enum_class, value).value  # type: ignore
    if hasattr(value, "value"):  # type: ignore
        return value.value  # type: ignore
    return value  # type: ignore


def _divide_by_64(value: int) -> int:
    """Divide by 64 and round to nearest int."""
    return int(round(value / 64))


def _build_string(builder: flatbuffers.Builder, value: str | None) -> int:
    """Build a FlatBuffer string, returning 0 if value is None."""
    if value is None:
        return 0
    return builder.CreateString(value)  # type: ignore


def _build_control(builder: flatbuffers.Builder, control: ControlDict) -> int:
    """Build a Control FlatBuffer object."""
    ControlStart(builder)

    if "file" in control:
        file_str = _build_string(builder, control["file"])
        ControlAddFile(builder, file_str)

    if "weight" in control:
        ControlAddWeight(builder, control["weight"])

    if "guidance_start" in control:
        ControlAddGuidanceStart(builder, control["guidance_start"])

    if "guidance_end" in control:
        ControlAddGuidanceEnd(builder, control["guidance_end"])

    if "no_prompt" in control:
        ControlAddNoPrompt(builder, control["no_prompt"])

    if "global_average_pooling" in control:
        ControlAddGlobalAveragePooling(builder, control["global_average_pooling"])

    if "down_sampling_rate" in control:
        ControlAddDownSamplingRate(builder, control["down_sampling_rate"])

    if "control_mode" in control:
        control_mode = _to_enum_value(control["control_mode"], ControlMode)
        ControlAddControlMode(builder, control_mode)

    if "target_blocks" in control:
        target_blocks = control["target_blocks"]
        ControlStartTargetBlocksVector(builder, len(target_blocks))  # type: ignore
        for block in reversed(target_blocks):
            builder.PrependUOffsetTRelative(_build_string(builder, block))  # type: ignore
        target_blocks_vec = builder.EndVector()  # type: ignore
        ControlAddTargetBlocks(builder, target_blocks_vec)

    if "input_override" in control:
        input_override = _to_enum_value(control["input_override"], ControlInputType)
        ControlAddInputOverride(builder, input_override)

    return ControlEnd(builder)  # type: ignore


def _build_lora(builder: flatbuffers.Builder, lora: LoraDict) -> int:
    """Build a LoRA FlatBuffer object."""
    LoRAStart(builder)

    if "file" in lora:
        file_str = _build_string(builder, lora["file"])
        LoRAAddFile(builder, file_str)

    if "weight" in lora:
        LoRAAddWeight(builder, lora["weight"])

    if "mode" in lora:
        mode = _to_enum_value(lora["mode"], LoRAMode)
        LoRAAddMode(builder, mode)

    return LoRAEnd(builder)  # type: ignore


def build_config(config: ConfigDict, seed: int | None = None) -> bytes:
    """Build a FlatBuffer GenerationConfiguration from a ConfigDict."""
    builder = flatbuffers.Builder(1024)

    # Build nested structures first (controls and loras)
    controls_offset = 0
    if "controls" in config and config["controls"]:
        controls = config["controls"]
        GenerationConfigurationStartControlsVector(builder, len(controls))  # type: ignore
        for control in reversed(controls):
            builder.PrependUOffsetTRelative(_build_control(builder, control))  # type: ignore
        controls_offset = builder.EndVector()  # type: ignore

    loras_offset = 0
    if "loras" in config and config["loras"]:
        loras = config["loras"]
        GenerationConfigurationStartLorasVector(builder, len(loras))  # type: ignore
        for lora in reversed(loras):
            builder.PrependUOffsetTRelative(_build_lora(builder, lora))  # type: ignore
        loras_offset = builder.EndVector()  # type: ignore

    # Build string fields
    model_str = _build_string(builder, config.get("model"))
    refiner_model_str = _build_string(builder, config.get("refiner_model"))
    upscaler_str = _build_string(builder, config.get("upscaler"))
    face_restoration_str = _build_string(builder, config.get("face_restoration"))
    name_str = _build_string(builder, config.get("name"))
    clip_l_text_str = _build_string(builder, config.get("clip_l_text"))
    open_clip_g_text_str = _build_string(builder, config.get("open_clip_g_text"))
    t5_text_str = _build_string(builder, config.get("t5_text"))

    # Start the main object
    GenerationConfigurationStart(builder)

    # Core generation fields
    if "width" in config:
        width = _divide_by_64(config["width"])
        GenerationConfigurationAddStartWidth(builder, width)

    if "height" in config:
        height = _divide_by_64(config["height"])
        GenerationConfigurationAddStartHeight(builder, height)

    # Handle seed override
    seed_value = seed if seed is not None else config.get("seed")
    if seed_value is not None:
        GenerationConfigurationAddSeed(builder, seed_value)

    if "steps" in config:
        GenerationConfigurationAddSteps(builder, config["steps"])

    if "guidance" in config:
        GenerationConfigurationAddGuidanceScale(builder, config["guidance"])
    elif "guidance_scale" in config:
        GenerationConfigurationAddGuidanceScale(builder, config["guidance_scale"])

    if "image_guidance_scale" in config:
        GenerationConfigurationAddImageGuidanceScale(
            builder, config["image_guidance_scale"]
        )

    if "strength" in config:
        GenerationConfigurationAddStrength(builder, config["strength"])

    if model_str:
        GenerationConfigurationAddModel(builder, model_str)

    if "sampler" in config:
        sampler = _to_enum_value(config["sampler"], SamplerType)
        GenerationConfigurationAddSampler(builder, sampler)

    if "batch_size" in config:
        GenerationConfigurationAddBatchSize(builder, config["batch_size"])

    if "hires_fix" in config:
        GenerationConfigurationAddHiresFix(builder, config["hires_fix"])

    if "hires_fix_width" in config:
        hires_fix_width = _divide_by_64(config["hires_fix_width"])
        GenerationConfigurationAddHiresFixStartWidth(builder, hires_fix_width)

    if "hires_fix_height" in config:
        hires_fix_height = _divide_by_64(config["hires_fix_height"])
        GenerationConfigurationAddHiresFixStartHeight(builder, hires_fix_height)

    if "hires_fix_strength" in config:
        GenerationConfigurationAddHiresFixStrength(
            builder, config["hires_fix_strength"]
        )

    if upscaler_str:
        GenerationConfigurationAddUpscaler(builder, upscaler_str)

    # seed_mode defaults to ScaleAlike if not provided
    seed_mode_value = config.get("seed_mode")
    if seed_mode_value is not None:
        seed_mode = _to_enum_value(seed_mode_value, SeedMode)
    else:
        seed_mode = SeedMode.ScaleAlike.value
    GenerationConfigurationAddSeedMode(builder, seed_mode)

    if "clip_skip" in config:
        GenerationConfigurationAddClipSkip(builder, config["clip_skip"])

    if controls_offset:
        GenerationConfigurationAddControls(builder, controls_offset)

    if loras_offset:
        GenerationConfigurationAddLoras(builder, loras_offset)

    if "mask_blur" in config:
        GenerationConfigurationAddMaskBlur(builder, config["mask_blur"])

    if face_restoration_str:
        GenerationConfigurationAddFaceRestoration(builder, face_restoration_str)

    if "negative_prompt_for_image_prior" in config:
        GenerationConfigurationAddNegativePromptForImagePrior(
            builder, config["negative_prompt_for_image_prior"]
        )

    if refiner_model_str:
        GenerationConfigurationAddRefinerModel(builder, refiner_model_str)

    if "original_image_height" in config:
        original_image_height = _divide_by_64(config["original_image_height"])
        GenerationConfigurationAddOriginalImageHeight(builder, original_image_height)

    if "original_image_width" in config:
        original_image_width = _divide_by_64(config["original_image_width"])
        GenerationConfigurationAddOriginalImageWidth(builder, original_image_width)

    if "crop_top" in config:
        crop_top = _divide_by_64(config["crop_top"])
        GenerationConfigurationAddCropTop(builder, crop_top)

    if "crop_left" in config:
        crop_left = _divide_by_64(config["crop_left"])
        GenerationConfigurationAddCropLeft(builder, crop_left)

    if "target_image_height" in config:
        target_image_height = _divide_by_64(config["target_image_height"])
        GenerationConfigurationAddTargetImageHeight(builder, target_image_height)

    if "target_image_width" in config:
        target_image_width = _divide_by_64(config["target_image_width"])
        GenerationConfigurationAddTargetImageWidth(builder, target_image_width)

    if "aesthetic_score" in config:
        GenerationConfigurationAddAestheticScore(builder, config["aesthetic_score"])

    if "negative_aesthetic_score" in config:
        GenerationConfigurationAddNegativeAestheticScore(
            builder, config["negative_aesthetic_score"]
        )

    if "zero_negative_prompt" in config:
        GenerationConfigurationAddZeroNegativePrompt(
            builder, config["zero_negative_prompt"]
        )

    if "refiner_start" in config:
        GenerationConfigurationAddRefinerStart(builder, config["refiner_start"])

    if "negative_original_image_height" in config:
        negative_original_image_height = _divide_by_64(
            config["negative_original_image_height"]
        )
        GenerationConfigurationAddNegativeOriginalImageHeight(
            builder, negative_original_image_height
        )

    if "negative_original_image_width" in config:
        negative_original_image_width = _divide_by_64(
            config["negative_original_image_width"]
        )
        GenerationConfigurationAddNegativeOriginalImageWidth(
            builder, negative_original_image_width
        )

    if name_str:
        GenerationConfigurationAddName(builder, name_str)

    if "fps_id" in config:
        GenerationConfigurationAddFpsId(builder, config["fps_id"])

    if "motion_scale" in config:
        GenerationConfigurationAddMotionBucketId(builder, config["motion_scale"])

    if "guiding_frame_noise" in config:
        GenerationConfigurationAddCondAug(builder, config["guiding_frame_noise"])

    if "start_frame_guidance" in config:
        GenerationConfigurationAddStartFrameCfg(builder, config["start_frame_guidance"])

    if "num_frames" in config:
        GenerationConfigurationAddNumFrames(builder, config["num_frames"])

    if "mask_blur_outset" in config:
        GenerationConfigurationAddMaskBlurOutset(builder, config["mask_blur_outset"])

    if "sharpness" in config:
        GenerationConfigurationAddSharpness(builder, config["sharpness"])

    if "shift" in config:
        GenerationConfigurationAddShift(builder, config["shift"])

    if "tiled_decoding" in config:
        GenerationConfigurationAddTiledDecoding(builder, config["tiled_decoding"])

    if "decoding_tile_width" in config:
        decoding_tile_width = _divide_by_64(config["decoding_tile_width"])
        GenerationConfigurationAddDecodingTileWidth(builder, decoding_tile_width)

    if "decoding_tile_height" in config:
        decoding_tile_height = _divide_by_64(config["decoding_tile_height"])
        GenerationConfigurationAddDecodingTileHeight(builder, decoding_tile_height)

    if "decoding_tile_overlap" in config:
        decoding_tile_overlap = _divide_by_64(config["decoding_tile_overlap"])
        GenerationConfigurationAddDecodingTileOverlap(builder, decoding_tile_overlap)

    if "stochastic_sampling_gamma" in config:
        GenerationConfigurationAddStochasticSamplingGamma(
            builder, config["stochastic_sampling_gamma"]
        )

    if "preserve_original_after_inpaint" in config:
        GenerationConfigurationAddPreserveOriginalAfterInpaint(
            builder, config["preserve_original_after_inpaint"]
        )

    if "tiled_diffusion" in config:
        GenerationConfigurationAddTiledDiffusion(builder, config["tiled_diffusion"])

    if "diffusion_tile_width" in config:
        diffusion_tile_width = _divide_by_64(config["diffusion_tile_width"])
        GenerationConfigurationAddDiffusionTileWidth(builder, diffusion_tile_width)

    if "diffusion_tile_height" in config:
        diffusion_tile_height = _divide_by_64(config["diffusion_tile_height"])
        GenerationConfigurationAddDiffusionTileHeight(builder, diffusion_tile_height)

    if "diffusion_tile_overlap" in config:
        diffusion_tile_overlap = _divide_by_64(config["diffusion_tile_overlap"])
        GenerationConfigurationAddDiffusionTileOverlap(builder, diffusion_tile_overlap)

    if "upscaler_scale_factor" in config:
        GenerationConfigurationAddUpscalerScaleFactor(
            builder, config["upscaler_scale_factor"]
        )

    if "t5_text_encoder" in config:
        GenerationConfigurationAddT5TextEncoder(builder, config["t5_text_encoder"])

    if "separate_clip_l" in config:
        GenerationConfigurationAddSeparateClipL(builder, config["separate_clip_l"])

    if clip_l_text_str:
        GenerationConfigurationAddClipLText(builder, clip_l_text_str)

    if "separate_open_clip_g" in config:
        GenerationConfigurationAddSeparateOpenClipG(
            builder, config["separate_open_clip_g"]
        )

    if open_clip_g_text_str:
        GenerationConfigurationAddOpenClipGText(builder, open_clip_g_text_str)

    if "speed_up_with_guidance_embed" in config:
        GenerationConfigurationAddSpeedUpWithGuidanceEmbed(
            builder, config["speed_up_with_guidance_embed"]
        )

    if "guidance_embed" in config:
        GenerationConfigurationAddGuidanceEmbed(builder, config["guidance_embed"])

    if "resolution_dependent_shift" in config:
        GenerationConfigurationAddResolutionDependentShift(
            builder, config["resolution_dependent_shift"]
        )

    if "tea_cache_start" in config:
        GenerationConfigurationAddTeaCacheStart(builder, config["tea_cache_start"])

    if "tea_cache_end" in config:
        GenerationConfigurationAddTeaCacheEnd(builder, config["tea_cache_end"])

    if "tea_cache_threshold" in config:
        GenerationConfigurationAddTeaCacheThreshold(
            builder, config["tea_cache_threshold"]
        )

    if "tea_cache" in config:
        GenerationConfigurationAddTeaCache(builder, config["tea_cache"])

    if "separate_t5" in config:
        GenerationConfigurationAddSeparateT5(builder, config["separate_t5"])

    if t5_text_str:
        GenerationConfigurationAddT5Text(builder, t5_text_str)

    if "tea_cache_max_skip_steps" in config:
        GenerationConfigurationAddTeaCacheMaxSkipSteps(
            builder, config["tea_cache_max_skip_steps"]
        )

    if "causal_inference_enabled" in config:
        GenerationConfigurationAddCausalInferenceEnabled(
            builder, config["causal_inference_enabled"]
        )

    if "causal_inference" in config:
        GenerationConfigurationAddCausalInference(builder, config["causal_inference"])

    if "causal_inference_pad" in config:
        GenerationConfigurationAddCausalInferencePad(
            builder, config["causal_inference_pad"]
        )

    if "cfg_zero_star" in config:
        GenerationConfigurationAddCfgZeroStar(builder, config["cfg_zero_star"])

    if "cfg_zero_init_steps" in config:
        GenerationConfigurationAddCfgZeroInitSteps(
            builder, config["cfg_zero_init_steps"]
        )

    if "compression_artifacts" in config:
        compression_artifacts = _to_enum_value(
            config["compression_artifacts"], CompressionMethod
        )
        GenerationConfigurationAddCompressionArtifacts(builder, compression_artifacts)

    if "compression_artifacts_quality" in config:
        GenerationConfigurationAddCompressionArtifactsQuality(
            builder, config["compression_artifacts_quality"]
        )

    # End the object
    config_offset = GenerationConfigurationEnd(builder)  # type: ignore

    # Finish the buffer
    _ = builder.Finish(config_offset)  # type: ignore

    return bytes(builder.Output())
