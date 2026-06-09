from typing import Unpack, cast, Any
import json
import flatbuffers
from drawthings_py.configs.config_dict import ConfigDict, ConfigKey
from drawthings_py.configs.config_generated import GenConfig
from drawthings_py.generated.dt_grpc.config_generated import GenerationConfigurationT, LoRAT, ControlT
from drawthings_py.configs.types import CompressionMethod

json_key_map: dict[str, ConfigKey] = {
    "id": "id",
    "start_width": "width",
    "width": "width",
    "startWidth": "width",
    "height": "height",
    "startHeight": "height",
    "start_height": "height",
    "seed": "seed",
    "steps": "steps",
    "guidanceScale": "guidance",
    "guidance": "guidance",
    "guidance_scale": "guidance",
    "strength": "strength",
    "model": "model",
    "sampler": "sampler",
    "loras": "loras",
    "controls": "controls",
    "batch_count": "batch_count",
    "batchCount": "batch_count",
    "batch_size": "batch_size",
    "batchSize": "batch_size",
    "hires_fix": "hires_fix",
    "hires_fix_start_width": "hires_fix_width",
    "hires_fix_width": "hires_fix_width",
    "hiresFixWidth": "hires_fix_width",
    "hiresFixHeight": "hires_fix_height",
    "hires_fix_start_height": "hires_fix_height",
    "hires_fix_height": "hires_fix_height",
    "hires_fix_strength": "hires_fix_strength",
    "hiresFixStrength": "hires_fix_strength",
    "upscaler": "upscaler",
    "image_guidance_scale": "image_guidance_scale",
    "imageGuidanceScale": "image_guidance_scale",
    "seedMode": "seed_mode",
    "seed_mode": "seed_mode",
    "clip_skip": "clip_skip",
    "clipSkip": "clip_skip",
    "mask_blur": "mask_blur",
    "maskBlur": "mask_blur",
    "faceRestoration": "face_restoration",
    "face_restoration": "face_restoration",
    "decodeWithAttention": "decode_with_attention",
    "decode_with_attention": "decode_with_attention",
    "hires_fix_decode_with_attention": "hires_fix_decode_with_attention",
    "hiresFixDecodeWithAttention": "hires_fix_decode_with_attention",
    "clipWeight": "clip_weight",
    "clip_weight": "clip_weight",
    "negative_prompt_for_image_prior": "negative_prompt_for_image_prior",
    "negativePromptForImagePrior": "negative_prompt_for_image_prior",
    "image_prior_steps": "image_prior_steps",
    "imagePriorSteps": "image_prior_steps",
    "refinerModel": "refiner_model",
    "refiner_model": "refiner_model",
    "original_image_height": "original_image_height",
    "originalImageHeight": "original_image_height",
    "originalImageWidth": "original_image_width",
    "original_image_width": "original_image_width",
    "cropTop": "crop_top",
    "crop_top": "crop_top",
    "cropLeft": "crop_left",
    "crop_left": "crop_left",
    "targetImageHeight": "target_image_height",
    "target_image_height": "target_image_height",
    "targetImageWidth": "target_image_width",
    "target_image_width": "target_image_width",
    "aestheticScore": "aesthetic_score",
    "aesthetic_score": "aesthetic_score",
    "negativeAestheticScore": "negative_aesthetic_score",
    "negative_aesthetic_score": "negative_aesthetic_score",
    "zeroNegativePrompt": "zero_negative_prompt",
    "zero_negative_prompt": "zero_negative_prompt",
    "refinerStart": "refiner_start",
    "refiner_start": "refiner_start",
    "negative_original_image_height": "negative_original_image_height",
    "negativeOriginalImageHeight": "negative_original_image_height",
    "negativeOriginalImageWidth": "negative_original_image_width",
    "negative_original_image_width": "negative_original_image_width",
    "name": "name",
    "fps": "fps",
    "fpsId": "fps",
    "fps_id": "fps",
    "motion_scale": "motion_scale",
    "motion_bucket_id": "motion_scale",
    "motionScale": "motion_scale",
    "guidingFrameNoise": "guiding_frame_noise",
    "cond_aug": "guiding_frame_noise",
    "guiding_frame_noise": "guiding_frame_noise",
    "start_frame_cfg": "guiding_frame_guidance",
    "guidingFrameGuidance": "guiding_frame_guidance",
    "guiding_frame_guidance": "guiding_frame_guidance",
    "num_frames": "num_frames",
    "numFrames": "num_frames",
    "mask_blur_outset": "mask_blur_outset",
    "maskBlurOutset": "mask_blur_outset",
    "sharpness": "sharpness",
    "shift": "shift",
    "stage_2_steps": "stage_2_steps",
    "stage2Steps": "stage_2_steps",
    "stage_2_cfg": "stage_2_cfg",
    "stage2Cfg": "stage_2_cfg",
    "stage2Shift": "stage_2_shift",
    "stage_2_shift": "stage_2_shift",
    "tiledDecoding": "tiled_decoding",
    "tiled_decoding": "tiled_decoding",
    "decoding_tile_width": "decoding_tile_width",
    "decodingTileWidth": "decoding_tile_width",
    "decodingTileHeight": "decoding_tile_height",
    "decoding_tile_height": "decoding_tile_height",
    "decoding_tile_overlap": "decoding_tile_overlap",
    "decodingTileOverlap": "decoding_tile_overlap",
    "stochasticSamplingGamma": "stochastic_sampling_gamma",
    "stochastic_sampling_gamma": "stochastic_sampling_gamma",
    "preserveOriginalAfterInpaint": "preserve_original_after_inpaint",
    "preserve_original_after_inpaint": "preserve_original_after_inpaint",
    "tiledDiffusion": "tiled_diffusion",
    "tiled_diffusion": "tiled_diffusion",
    "diffusion_tile_width": "diffusion_tile_width",
    "diffusionTileWidth": "diffusion_tile_width",
    "diffusionTileHeight": "diffusion_tile_height",
    "diffusion_tile_height": "diffusion_tile_height",
    "diffusion_tile_overlap": "diffusion_tile_overlap",
    "diffusionTileOverlap": "diffusion_tile_overlap",
    "upscalerScaleFactor": "upscaler_scale_factor",
    "upscaler_scale_factor": "upscaler_scale_factor",
    "t5_text_encoder": "t5_text_encoder",
    "t5TextEncoder": "t5_text_encoder",
    "separate_clip_l": "separate_clip_l",
    "separateClipL": "separate_clip_l",
    "clip_l_text": "clip_l_text",
    "clipLText": "clip_l_text",
    "separate_open_clip_g": "separate_open_clip_g",
    "separateOpenClipG": "separate_open_clip_g",
    "open_clip_g_text": "open_clip_g_text",
    "openClipGText": "open_clip_g_text",
    "speed_up_with_guidance_embed": "speed_up_with_guidance_embed",
    "speedUpWithGuidanceEmbed": "speed_up_with_guidance_embed",
    "guidance_embed": "guidance_embed",
    "guidanceEmbed": "guidance_embed",
    "resolutionDependentShift": "resolution_dependent_shift",
    "resolution_dependent_shift": "resolution_dependent_shift",
    "teaCacheStart": "tea_cache_start",
    "tea_cache_start": "tea_cache_start",
    "tea_cache_end": "tea_cache_end",
    "teaCacheEnd": "tea_cache_end",
    "tea_cache_threshold": "tea_cache_threshold",
    "teaCacheThreshold": "tea_cache_threshold",
    "teaCache": "tea_cache",
    "tea_cache": "tea_cache",
    "separate_t5": "separate_t5",
    "separateT5": "separate_t5",
    "t5Text": "t5_text",
    "t5_text": "t5_text",
    "teaCacheMaxSkipSteps": "tea_cache_max_skip_steps",
    "tea_cache_max_skip_steps": "tea_cache_max_skip_steps",
    "causal_inference_enabled": "causal_inference_enabled",
    "causalInferenceEnabled": "causal_inference_enabled",
    "causal_inference": "causal_inference",
    "causalInference": "causal_inference",
    "causalInferencePad": "causal_inference_pad",
    "causal_inference_pad": "causal_inference_pad",
    "cfgZeroStar": "cfg_zero_star",
    "cfg_zero_star": "cfg_zero_star",
    "cfg_zero_init_steps": "cfg_zero_init_steps",
    "cfgZeroInitSteps": "cfg_zero_init_steps",
    "compression_artifacts": "compression_artifacts",
    "compressionArtifacts": "compression_artifacts",
    "compressionArtifactsQuality": "compression_artifacts_quality",
    "compression_artifacts_quality": "compression_artifacts_quality",
}


def from_json(json_text: str | None = None, json_data: ConfigDict | None = None) -> GenConfig:
    data = json_data if json_data is not None else cast(dict[str, Any], json.loads(json_text or "{}"))  # pyright: ignore[reportExplicitAny]
    config: ConfigDict = {}
    for key, value in data.items():
        if mapped_key := json_key_map.get(key):
            config[mapped_key] = value # pyright: ignore[reportGeneralTypeIssues]
    return GenConfig(**config)


def to_fbs(config: GenConfig, seed: int | None = None) -> bytes:
    builder = flatbuffers.Builder(0)
    config_t = GenerationConfigurationT()

    config_t.seed = seed or config["seed"]

    config_t.startWidth = config["width"]
    config_t.startHeight = config["height"]
    config_t.steps = config["steps"]
    config_t.guidanceScale = config["guidance"]
    config_t.strength = config["strength"]
    config_t.model = config["model"]
    config_t.sampler = config["sampler"]
    config_t.loras = [LoRAT(**lora) for lora in config["loras"]]
    config_t.controls = [ControlT(**control) for control in config["controls"]]
    config_t.batchSize = config["batch_size"]
    config_t.hiresFix = config["hires_fix"]
    if not config["hires_fix"]:
        config_t.hiresFixStartWidth = config["hires_fix_width"]
    if not config["hires_fix"]:
        config_t.hiresFixStartHeight = config["hires_fix_height"]
    if not config["hires_fix"]:
        config_t.hiresFixStrength = config["hires_fix_strength"]
    config_t.upscaler = config["upscaler"]
    config_t.imageGuidanceScale = config["image_guidance_scale"]
    config_t.seedMode = config["seed_mode"]
    config_t.clipSkip = config["clip_skip"]
    config_t.maskBlur = config["mask_blur"]
    config_t.faceRestoration = config["face_restoration"]
    config_t.refinerModel = config["refiner_model"]
    config_t.originalImageHeight = config["original_image_height"]
    config_t.originalImageWidth = config["original_image_width"]
    config_t.cropTop = config["crop_top"]
    config_t.cropLeft = config["crop_left"]
    config_t.targetImageHeight = config["target_image_height"]
    config_t.targetImageWidth = config["target_image_width"]
    config_t.zeroNegativePrompt = config["zero_negative_prompt"]
    if not config["refiner_model"]:
        config_t.refinerStart = config["refiner_start"]
    config_t.negativeOriginalImageHeight = config["negative_original_image_height"]
    config_t.negativeOriginalImageWidth = config["negative_original_image_width"]
    config_t.fpsId = config["fps"]
    config_t.motionBucketId = config["motion_scale"]
    config_t.condAug = config["guiding_frame_noise"]
    config_t.startFrameCfg = config["guiding_frame_guidance"]
    config_t.numFrames = config["num_frames"]
    config_t.maskBlurOutset = config["mask_blur_outset"]
    config_t.sharpness = config["sharpness"]
    config_t.shift = config["shift"]
    config_t.tiledDecoding = config["tiled_decoding"]
    if not config["tiled_decoding"]:
        config_t.decodingTileWidth = config["decoding_tile_width"]
    if not config["tiled_decoding"]:
        config_t.decodingTileHeight = config["decoding_tile_height"]
    if not config["tiled_decoding"]:
        config_t.decodingTileOverlap = config["decoding_tile_overlap"]
    if not config["sampler"]:
        config_t.stochasticSamplingGamma = config["stochastic_sampling_gamma"]
    config_t.preserveOriginalAfterInpaint = config["preserve_original_after_inpaint"]
    config_t.tiledDiffusion = config["tiled_diffusion"]
    if not config["tiled_diffusion"]:
        config_t.diffusionTileWidth = config["diffusion_tile_width"]
    if not config["tiled_diffusion"]:
        config_t.diffusionTileHeight = config["diffusion_tile_height"]
    if not config["tiled_diffusion"]:
        config_t.diffusionTileOverlap = config["diffusion_tile_overlap"]
    if not config["upscaler"]:
        config_t.upscalerScaleFactor = config["upscaler_scale_factor"]
    config_t.t5TextEncoder = config["t5_text_encoder"]
    config_t.separateClipL = config["separate_clip_l"]
    if not config["separate_clip_l"]:
        config_t.clipLText = config["clip_l_text"]
    config_t.separateOpenClipG = config["separate_open_clip_g"]
    if not config["separate_open_clip_g"]:
        config_t.openClipGText = config["open_clip_g_text"]
    config_t.speedUpWithGuidanceEmbed = config["speed_up_with_guidance_embed"]
    if config["speed_up_with_guidance_embed"]:
        config_t.guidanceEmbed = config["guidance_embed"]
    config_t.resolutionDependentShift = config["resolution_dependent_shift"]
    if not config["tea_cache"]:
        config_t.teaCacheStart = config["tea_cache_start"]
    if not config["tea_cache"]:
        config_t.teaCacheEnd = config["tea_cache_end"]
    if not config["tea_cache"]:
        config_t.teaCacheThreshold = config["tea_cache_threshold"]
    config_t.teaCache = config["tea_cache"]
    config_t.separateT5 = config["separate_t5"]
    if not config["separate_t5"]:
        config_t.t5Text = config["t5_text"]
    if not config["tea_cache"]:
        config_t.teaCacheMaxSkipSteps = config["tea_cache_max_skip_steps"]
    config_t.causalInferenceEnabled = config["causal_inference_enabled"]
    if not config["causal_inference_enabled"]:
        config_t.causalInference = config["causal_inference"]
    if not config["causal_inference_enabled"]:
        config_t.causalInferencePad = config["causal_inference_pad"]
    config_t.cfgZeroStar = config["cfg_zero_star"]
    if not config["cfg_zero_star"]:
        config_t.cfgZeroInitSteps = config["cfg_zero_init_steps"]
    config_t.compressionArtifacts = config["compression_artifacts"]
    if config["compression_artifacts"] == CompressionMethod.Disabled:
        config_t.compressionArtifactsQuality = config["compression_artifacts_quality"]

    fbs_config = config_t.Pack(builder)
    builder.Finish(fbs_config) # pyright: ignore[reportUnknownMemberType, reportUnusedCallResult]
    return bytes(builder.Output()) 