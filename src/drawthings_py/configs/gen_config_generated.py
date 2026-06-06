from __future__ import annotations
from .types import SamplerType, SeedMode, CompressionMethod, UpscalerModel
import json
from typing import cast, Any, TypedDict


class ConfigDict(TypedDict, total=False):
    id: int
    width: int
    height: int
    seed: int
    steps: int
    guidance: float
    strength: float
    model: str | None
    sampler: SamplerType
    batch_count: int
    batch_size: int
    hires_fix: bool
    hires_fix_width: int
    hires_fix_height: int
    hires_fix_strength: float
    upscaler: UpscalerModel | None
    image_guidance_scale: float
    seed_mode: SeedMode
    clip_skip: int
    mask_blur: float
    face_restoration: str | None
    decode_with_attention: bool
    hires_fix_decode_with_attention: bool
    clip_weight: float
    negative_prompt_for_image_prior: bool
    image_prior_steps: int
    refiner_model: str | None
    original_image_height: int
    original_image_width: int
    crop_top: int
    crop_left: int
    target_image_height: int
    target_image_width: int
    aesthetic_score: float
    negative_aesthetic_score: float
    zero_negative_prompt: bool
    refiner_start: float
    negative_original_image_height: int
    negative_original_image_width: int
    name: str | None
    fps: int
    motion_scale: int
    guiding_frame_noise: float
    guiding_frame_guidance: float
    num_frames: int
    mask_blur_outset: int
    sharpness: float
    shift: float
    stage_2_steps: int
    stage_2_cfg: float
    stage_2_shift: float
    tiled_decoding: bool
    decoding_tile_width: int
    decoding_tile_height: int
    decoding_tile_overlap: int
    stochastic_sampling_gamma: float
    preserve_original_after_inpaint: bool
    tiled_diffusion: bool
    diffusion_tile_width: int
    diffusion_tile_height: int
    diffusion_tile_overlap: int
    upscaler_scale_factor: int
    t5_text_encoder: bool
    separate_clip_l: bool
    clip_l_text: str | None
    separate_open_clip_g: bool
    open_clip_g_text: str | None
    speed_up_with_guidance_embed: bool
    guidance_embed: float
    resolution_dependent_shift: bool
    tea_cache_start: int
    tea_cache_end: int
    tea_cache_threshold: float
    tea_cache: bool
    separate_t5: bool
    t5_text: str | None
    tea_cache_max_skip_steps: int
    causal_inference_enabled: bool
    causal_inference: int
    causal_inference_pad: int
    cfg_zero_star: bool
    cfg_zero_init_steps: int
    compression_artifacts: CompressionMethod
    compression_artifacts_quality: float


class GenConfig:
    _data: ConfigDict

    def __init__(self, data: ConfigDict | None = None):
        self._data = data or ConfigDict()

    @property
    def width(self) -> int:
        """Width of the image in pixels (will be rounded to the nearest 64)"""
        return self._data.get("width", int())

    @width.setter
    def width(self, value: int):
        self._data["width"] = value

    @property
    def height(self) -> int:
        """Height of the image in pixels (will be rounded to the nearest 64)"""
        return self._data.get("height", int())

    @height.setter
    def height(self, value: int):
        self._data["height"] = value

    @property
    def seed(self) -> int:
        """controls the random number generation for the diffusion process, enabling reproducible image outputs when the same seed is used with identical parameters"""
        return self._data.get("seed", -1)

    @seed.setter
    def seed(self, value: int):
        self._data["seed"] = value

    @property
    def steps(self) -> int:
        """specifies the number of sampling iterations (denoising steps) performed during the image generation process"""
        return self._data.get("steps", int())

    @steps.setter
    def steps(self, value: int):
        self._data["steps"] = value

    @property
    def guidance(self) -> float:
        """controls how strongly the generation follows the text prompt (also called CFG or text guidance)"""
        return self._data.get("guidance", 4.5)

    @guidance.setter
    def guidance(self, value: float):
        self._data["guidance"] = value

    @property
    def strength(self) -> float:
        """determines the denoising strength for img2img operations"""
        return self._data.get("strength", float())

    @strength.setter
    def strength(self, value: float):
        self._data["strength"] = value

    @property
    def model(self) -> str | None:
        """specifies which model file to use for generation"""
        return self._data.get("model", str())

    @model.setter
    def model(self, value: str | None):
        self._data["model"] = value

    @property
    def sampler(self) -> SamplerType:
        """specifies the sampling algorithm and schedule to use for generation"""
        return SamplerType(
            cast(int, self._data.get("sampler", SamplerType.DPMPP2MKarras))
        )

    @sampler.setter
    def sampler(self, value: SamplerType):
        self._data["sampler"] = value

    @property
    def batch_size(self) -> int:
        """number of images to generate in a single batch"""
        return self._data.get("batch_size", 1)

    @batch_size.setter
    def batch_size(self, value: int):
        self._data["batch_size"] = value

    @property
    def hires_fix(self) -> bool:
        """enables high-resolution fix for generation. When enabled, image generation begins at a lower resoution, then switches to the full size at the specified point"""
        return self._data.get("hires_fix", False)

    @hires_fix.setter
    def hires_fix(self, value: bool):
        self._data["hires_fix"] = value

    @property
    def hires_fix_width(self) -> int:
        """width to use for the first-pass generation"""
        return self._data.get("hires_fix_width", 512)

    @hires_fix_width.setter
    def hires_fix_width(self, value: int):
        self._data["hires_fix_width"] = value

    @property
    def hires_fix_height(self) -> int:
        """height to use for the first-pass generation"""
        return self._data.get("hires_fix_height", 512)

    @hires_fix_height.setter
    def hires_fix_height(self, value: int):
        self._data["hires_fix_height"] = value

    @property
    def hires_fix_strength(self) -> float:
        """What percentage of steps are used in the full size generation"""
        return self._data.get("hires_fix_strength", 0.7)

    @hires_fix_strength.setter
    def hires_fix_strength(self, value: float):
        self._data["hires_fix_strength"] = value

    @property
    def upscaler(self) -> UpscalerModel | None:
        """specifies which upscaler model to use for generation"""
        return UpscalerModel(cast(str, self._data.get("upscaler", None)))

    @upscaler.setter
    def upscaler(self, value: UpscalerModel | None):
        self._data["upscaler"] = value

    @property
    def image_guidance_scale(self) -> float:
        """used with HiDream E-1 to determine how strongly the init image is followed Used with model version HiDream"""
        return self._data.get("image_guidance_scale", 1.5)

    @image_guidance_scale.setter
    def image_guidance_scale(self, value: float):
        self._data["image_guidance_scale"] = value

    @property
    def seed_mode(self) -> SeedMode:
        """specifies how seeds are used for batch generation"""
        return SeedMode(cast(int, self._data.get("seed_mode", SeedMode.ScaleAlike)))

    @seed_mode.setter
    def seed_mode(self, value: SeedMode):
        self._data["seed_mode"] = value

    @property
    def clip_skip(self) -> int:
        """clip_skip"""
        return self._data.get("clip_skip", 1)

    @clip_skip.setter
    def clip_skip(self, value: int):
        self._data["clip_skip"] = value

    @property
    def mask_blur(self) -> float:
        """mask_blur"""
        return self._data.get("mask_blur", float())

    @mask_blur.setter
    def mask_blur(self, value: float):
        self._data["mask_blur"] = value

    @property
    def face_restoration(self) -> str | None:
        """face_restoration"""
        return self._data.get("face_restoration", str())

    @face_restoration.setter
    def face_restoration(self, value: str | None):
        self._data["face_restoration"] = value

    @property
    def negative_prompt_for_image_prior(self) -> bool:
        """negative_prompt_for_image_prior"""
        return self._data.get("negative_prompt_for_image_prior", True)

    @negative_prompt_for_image_prior.setter
    def negative_prompt_for_image_prior(self, value: bool):
        self._data["negative_prompt_for_image_prior"] = value

    @property
    def refiner_model(self) -> str | None:
        """refiner_model"""
        return self._data.get("refiner_model", str())

    @refiner_model.setter
    def refiner_model(self, value: str | None):
        self._data["refiner_model"] = value

    @property
    def original_image_height(self) -> int:
        """The original height before image cropped during training (will be rounded to the nearest 64) Used with model versions SDXL and SDXL"""
        return self._data.get("original_image_height", int())

    @original_image_height.setter
    def original_image_height(self, value: int):
        self._data["original_image_height"] = value

    @property
    def original_image_width(self) -> int:
        """The original width before image cropped during training (will be rounded to the nearest 64) Used with model versions SDXL and SDXL"""
        return self._data.get("original_image_width", int())

    @original_image_width.setter
    def original_image_width(self, value: int):
        self._data["original_image_width"] = value

    @property
    def crop_top(self) -> int:
        """The top crop offset before image cropped during training (will be rounded to the nearest 64) Used with model versions SDXL and SDXL"""
        return self._data.get("crop_top", int())

    @crop_top.setter
    def crop_top(self, value: int):
        self._data["crop_top"] = value

    @property
    def crop_left(self) -> int:
        """The left crop offset before image cropped during training (will be rounded to the nearest 64) Used with model versions SDXL and SDXL"""
        return self._data.get("crop_left", int())

    @crop_left.setter
    def crop_left(self, value: int):
        self._data["crop_left"] = value

    @property
    def target_image_height(self) -> int:
        """The target height after image cropped during training (will be rounded to the nearest 64) Used with model versions SDXL and SDXL"""
        return self._data.get("target_image_height", int())

    @target_image_height.setter
    def target_image_height(self, value: int):
        self._data["target_image_height"] = value

    @property
    def target_image_width(self) -> int:
        """The target width after image cropped during training (will be rounded to the nearest 64) Used with model versions SDXL and SDXL"""
        return self._data.get("target_image_width", int())

    @target_image_width.setter
    def target_image_width(self, value: int):
        self._data["target_image_width"] = value

    @property
    def aesthetic_score(self) -> float:
        """aesthetic_score"""
        return self._data.get("aesthetic_score", 6)

    @aesthetic_score.setter
    def aesthetic_score(self, value: float):
        self._data["aesthetic_score"] = value

    @property
    def negative_aesthetic_score(self) -> float:
        """negative_aesthetic_score"""
        return self._data.get("negative_aesthetic_score", 2.5)

    @negative_aesthetic_score.setter
    def negative_aesthetic_score(self, value: float):
        self._data["negative_aesthetic_score"] = value

    @property
    def zero_negative_prompt(self) -> bool:
        """zero_negative_prompt Used with model versions Flux.1, HiDream, Pixart, SD3, SD3 Large, SDXL, SDXL and SSD"""
        return self._data.get("zero_negative_prompt", False)

    @zero_negative_prompt.setter
    def zero_negative_prompt(self, value: bool):
        self._data["zero_negative_prompt"] = value

    @property
    def refiner_start(self) -> float:
        """refiner_start"""
        return self._data.get("refiner_start", 0.7)

    @refiner_start.setter
    def refiner_start(self, value: float):
        self._data["refiner_start"] = value

    @property
    def negative_original_image_height(self) -> int:
        """The negative original image height (will be rounded to the nearest 64) Used with model versions SDXL and SDXL"""
        return self._data.get("negative_original_image_height", int())

    @negative_original_image_height.setter
    def negative_original_image_height(self, value: int):
        self._data["negative_original_image_height"] = value

    @property
    def negative_original_image_width(self) -> int:
        """The negative original image width (will be rounded to the nearest 64) Used with model versions SDXL and SDXL"""
        return self._data.get("negative_original_image_width", int())

    @negative_original_image_width.setter
    def negative_original_image_width(self, value: int):
        self._data["negative_original_image_width"] = value

    @property
    def name(self) -> str | None:
        """name"""
        return self._data.get("name", str())

    @name.setter
    def name(self, value: str | None):
        self._data["name"] = value

    @property
    def fps(self) -> int:
        """fps Used with model version SVD"""
        return self._data.get("fps", 5)

    @fps.setter
    def fps(self, value: int):
        self._data["fps"] = value

    @property
    def motion_scale(self) -> int:
        """motion_scale Used with model version SVD"""
        return self._data.get("motion_scale", 127)

    @motion_scale.setter
    def motion_scale(self, value: int):
        self._data["motion_scale"] = value

    @property
    def guiding_frame_noise(self) -> float:
        """guiding_frame_noise Used with model version SVD"""
        return self._data.get("guiding_frame_noise", 0.02)

    @guiding_frame_noise.setter
    def guiding_frame_noise(self, value: float):
        self._data["guiding_frame_noise"] = value

    @property
    def guiding_frame_guidance(self) -> float:
        """guiding_frame_guidance Used with model version SVD"""
        return self._data.get("guiding_frame_guidance", 1.0)

    @guiding_frame_guidance.setter
    def guiding_frame_guidance(self, value: float):
        self._data["guiding_frame_guidance"] = value

    @property
    def num_frames(self) -> int:
        """num_frames Used with model versions Hunyuan Video, LTX2, SVD, Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
        return self._data.get("num_frames", 14)

    @num_frames.setter
    def num_frames(self, value: int):
        self._data["num_frames"] = value

    @property
    def mask_blur_outset(self) -> int:
        """mask_blur_outset"""
        return self._data.get("mask_blur_outset", 0)

    @mask_blur_outset.setter
    def mask_blur_outset(self, value: int):
        self._data["mask_blur_outset"] = value

    @property
    def sharpness(self) -> float:
        """sharpness"""
        return self._data.get("sharpness", 0)

    @sharpness.setter
    def sharpness(self, value: float):
        self._data["sharpness"] = value

    @property
    def shift(self) -> float:
        """shift"""
        return self._data.get("shift", 1.0)

    @shift.setter
    def shift(self, value: float):
        self._data["shift"] = value

    @property
    def tiled_decoding(self) -> bool:
        """tiled_decoding"""
        return self._data.get("tiled_decoding", False)

    @tiled_decoding.setter
    def tiled_decoding(self, value: bool):
        self._data["tiled_decoding"] = value

    @property
    def decoding_tile_width(self) -> int:
        """The width of each tile for tiled decoding (will be rounded to the nearest 64)"""
        return self._data.get("decoding_tile_width", 10)

    @decoding_tile_width.setter
    def decoding_tile_width(self, value: int):
        self._data["decoding_tile_width"] = value

    @property
    def decoding_tile_height(self) -> int:
        """The height of each tile for tiled decoding (will be rounded to the nearest 64)"""
        return self._data.get("decoding_tile_height", 10)

    @decoding_tile_height.setter
    def decoding_tile_height(self, value: int):
        self._data["decoding_tile_height"] = value

    @property
    def decoding_tile_overlap(self) -> int:
        """The overlap between tiles for tiled decoding (will be rounded to the nearest 64)"""
        return self._data.get("decoding_tile_overlap", 2)

    @decoding_tile_overlap.setter
    def decoding_tile_overlap(self, value: int):
        self._data["decoding_tile_overlap"] = value

    @property
    def stochastic_sampling_gamma(self) -> float:
        """stochastic_sampling_gamma"""
        return self._data.get("stochastic_sampling_gamma", 0.3)

    @stochastic_sampling_gamma.setter
    def stochastic_sampling_gamma(self, value: float):
        self._data["stochastic_sampling_gamma"] = value

    @property
    def preserve_original_after_inpaint(self) -> bool:
        """preserve_original_after_inpaint"""
        return self._data.get("preserve_original_after_inpaint", True)

    @preserve_original_after_inpaint.setter
    def preserve_original_after_inpaint(self, value: bool):
        self._data["preserve_original_after_inpaint"] = value

    @property
    def tiled_diffusion(self) -> bool:
        """tiled_diffusion"""
        return self._data.get("tiled_diffusion", False)

    @tiled_diffusion.setter
    def tiled_diffusion(self, value: bool):
        self._data["tiled_diffusion"] = value

    @property
    def diffusion_tile_width(self) -> int:
        """The width of each tile for tiled diffusion (will be rounded to the nearest 64)"""
        return self._data.get("diffusion_tile_width", 16)

    @diffusion_tile_width.setter
    def diffusion_tile_width(self, value: int):
        self._data["diffusion_tile_width"] = value

    @property
    def diffusion_tile_height(self) -> int:
        """The height of each tile for tiled diffusion (will be rounded to the nearest 64)"""
        return self._data.get("diffusion_tile_height", 16)

    @diffusion_tile_height.setter
    def diffusion_tile_height(self, value: int):
        self._data["diffusion_tile_height"] = value

    @property
    def diffusion_tile_overlap(self) -> int:
        """The overlap between tiles for tiled diffusion (will be rounded to the nearest 64)"""
        return self._data.get("diffusion_tile_overlap", 2)

    @diffusion_tile_overlap.setter
    def diffusion_tile_overlap(self, value: int):
        self._data["diffusion_tile_overlap"] = value

    @property
    def upscaler_scale_factor(self) -> int:
        """upscaler_scale_factor"""
        return self._data.get("upscaler_scale_factor", 0)

    @upscaler_scale_factor.setter
    def upscaler_scale_factor(self, value: int):
        self._data["upscaler_scale_factor"] = value

    @property
    def t5_text_encoder(self) -> bool:
        """t5_text_encoder Used with model versions SD3 and SD3 Large"""
        return self._data.get("t5_text_encoder", True)

    @t5_text_encoder.setter
    def t5_text_encoder(self, value: bool):
        self._data["t5_text_encoder"] = value

    @property
    def separate_clip_l(self) -> bool:
        """separate_clip_l Used with model versions Flux.1, HiDream, SD3 and SD3 Large"""
        return self._data.get("separate_clip_l", False)

    @separate_clip_l.setter
    def separate_clip_l(self, value: bool):
        self._data["separate_clip_l"] = value

    @property
    def clip_l_text(self) -> str | None:
        """clip_l_text Used with model versions Flux.1, HiDream, SD3 and SD3 Large"""
        return self._data.get("clip_l_text", str())

    @clip_l_text.setter
    def clip_l_text(self, value: str | None):
        self._data["clip_l_text"] = value

    @property
    def separate_open_clip_g(self) -> bool:
        """separate_open_clip_g Used with model versions HiDream, SD3 and SD3 Large"""
        return self._data.get("separate_open_clip_g", False)

    @separate_open_clip_g.setter
    def separate_open_clip_g(self, value: bool):
        self._data["separate_open_clip_g"] = value

    @property
    def open_clip_g_text(self) -> str | None:
        """open_clip_g_text Used with model versions HiDream, SD3 and SD3 Large"""
        return self._data.get("open_clip_g_text", str())

    @open_clip_g_text.setter
    def open_clip_g_text(self, value: str | None):
        self._data["open_clip_g_text"] = value

    @property
    def speed_up_with_guidance_embed(self) -> bool:
        """speed_up_with_guidance_embed Used with model versions Flux.1, Flux.2, HiDream and Hunyuan Video"""
        return self._data.get("speed_up_with_guidance_embed", True)

    @speed_up_with_guidance_embed.setter
    def speed_up_with_guidance_embed(self, value: bool):
        self._data["speed_up_with_guidance_embed"] = value

    @property
    def guidance_embed(self) -> float:
        """guidance_embed Used with model versions Flux.1, Flux.2, HiDream and Hunyuan Video"""
        return self._data.get("guidance_embed", 3.5)

    @guidance_embed.setter
    def guidance_embed(self, value: float):
        self._data["guidance_embed"] = value

    @property
    def resolution_dependent_shift(self) -> bool:
        """resolution_dependent_shift Used with model versions Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Qwen, SD3, SD3 Large, Z Image and Cosmos2.5"""
        return self._data.get("resolution_dependent_shift", True)

    @resolution_dependent_shift.setter
    def resolution_dependent_shift(self, value: bool):
        self._data["resolution_dependent_shift"] = value

    @property
    def tea_cache_start(self) -> int:
        """tea_cache_start Used with model versions Flux.1, Hunyuan Video, Wan 2.1 and Wan 2.1"""
        return self._data.get("tea_cache_start", 5)

    @tea_cache_start.setter
    def tea_cache_start(self, value: int):
        self._data["tea_cache_start"] = value

    @property
    def tea_cache_end(self) -> int:
        """tea_cache_end Used with model versions Flux.1, Hunyuan Video, Wan 2.1 and Wan 2.1"""
        return self._data.get("tea_cache_end", -1)

    @tea_cache_end.setter
    def tea_cache_end(self, value: int):
        self._data["tea_cache_end"] = value

    @property
    def tea_cache_threshold(self) -> float:
        """tea_cache_threshold Used with model versions Flux.1, Hunyuan Video, Wan 2.1 and Wan 2.1"""
        return self._data.get("tea_cache_threshold", 0.06)

    @tea_cache_threshold.setter
    def tea_cache_threshold(self, value: float):
        self._data["tea_cache_threshold"] = value

    @property
    def tea_cache(self) -> bool:
        """tea_cache Used with model versions Flux.1, Hunyuan Video, Wan 2.1 and Wan 2.1"""
        return self._data.get("tea_cache", False)

    @tea_cache.setter
    def tea_cache(self, value: bool):
        self._data["tea_cache"] = value

    @property
    def separate_t5(self) -> bool:
        """separate_t5 Used with model version HiDream"""
        return self._data.get("separate_t5", False)

    @separate_t5.setter
    def separate_t5(self, value: bool):
        self._data["separate_t5"] = value

    @property
    def t5_text(self) -> str | None:
        """t5_text Used with model version HiDream"""
        return self._data.get("t5_text", str())

    @t5_text.setter
    def t5_text(self, value: str | None):
        self._data["t5_text"] = value

    @property
    def tea_cache_max_skip_steps(self) -> int:
        """tea_cache_max_skip_steps Used with model versions Flux.1, Hunyuan Video, Wan 2.1 and Wan 2.1"""
        return self._data.get("tea_cache_max_skip_steps", 3)

    @tea_cache_max_skip_steps.setter
    def tea_cache_max_skip_steps(self, value: int):
        self._data["tea_cache_max_skip_steps"] = value

    @property
    def causal_inference_enabled(self) -> bool:
        """causal_inference_enabled Used with model versions Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
        return self._data.get("causal_inference_enabled", False)

    @causal_inference_enabled.setter
    def causal_inference_enabled(self, value: bool):
        self._data["causal_inference_enabled"] = value

    @property
    def causal_inference(self) -> int:
        """causal_inference Used with model versions Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
        return self._data.get("causal_inference", 3)

    @causal_inference.setter
    def causal_inference(self, value: int):
        self._data["causal_inference"] = value

    @property
    def causal_inference_pad(self) -> int:
        """causal_inference_pad Used with model versions Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
        return self._data.get("causal_inference_pad", 0)

    @causal_inference_pad.setter
    def causal_inference_pad(self, value: int):
        self._data["causal_inference_pad"] = value

    @property
    def cfg_zero_star(self) -> bool:
        """cfg_zero_star Used with model versions Auraflow, Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Hunyuan Video, LTX2, Qwen, SD3, SD3 Large, Wan 2.1, Wan 2.1, Wan 2.2 5b, Z Image, Ernie Image and Cosmos2.5"""
        return self._data.get("cfg_zero_star", False)

    @cfg_zero_star.setter
    def cfg_zero_star(self, value: bool):
        self._data["cfg_zero_star"] = value

    @property
    def cfg_zero_init_steps(self) -> int:
        """cfg_zero_init_steps Used with model versions Auraflow, Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Hunyuan Video, LTX2, Qwen, SD3, SD3 Large, Wan 2.1, Wan 2.1, Wan 2.2 5b, Z Image, Ernie Image and Cosmos2.5"""
        return self._data.get("cfg_zero_init_steps", 0)

    @cfg_zero_init_steps.setter
    def cfg_zero_init_steps(self, value: int):
        self._data["cfg_zero_init_steps"] = value

    @property
    def compression_artifacts(self) -> CompressionMethod:
        """compression_artifacts Used with model versions Hunyuan Video, LTX2, Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
        return CompressionMethod(
            cast(
                int, self._data.get("compression_artifacts", CompressionMethod.Disabled)
            )
        )

    @compression_artifacts.setter
    def compression_artifacts(self, value: CompressionMethod):
        self._data["compression_artifacts"] = value

    @property
    def compression_artifacts_quality(self) -> float:
        """compression_artifacts_quality Used with model versions Hunyuan Video, LTX2, Wan 2.1, Wan 2.1 and Wan 2.2 5b"""
        return self._data.get("compression_artifacts_quality", 43.1)

    @compression_artifacts_quality.setter
    def compression_artifacts_quality(self, value: float):
        self._data["compression_artifacts_quality"] = value

    @classmethod
    def from_json(cls, json_text: str) -> GenConfig:
        data = cast(dict[str, Any], json.loads(json_text))  # pyright: ignore[reportExplicitAny]
        config_dict = ConfigDict()

        if id := data.get("id", data.get("id", None)):
            config_dict["id"] = id

        if width := data.get(
            "width",
            data.get("start_width", data.get("width", data.get("startWidth", None))),
        ):
            config_dict["width"] = width

        if height := data.get(
            "height",
            data.get("start_height", data.get("height", data.get("startHeight", None))),
        ):
            config_dict["height"] = height

        if seed := data.get("seed", data.get("seed", None)):
            config_dict["seed"] = seed

        if steps := data.get("steps", data.get("steps", None)):
            config_dict["steps"] = steps

        if guidance := data.get(
            "guidance", data.get("guidance_scale", data.get("guidanceScale", None))
        ):
            config_dict["guidance"] = guidance

        if strength := data.get("strength", data.get("strength", None)):
            config_dict["strength"] = strength

        if model := data.get("model", data.get("model", None)):
            config_dict["model"] = model

        if sampler := data.get("sampler", data.get("sampler", None)):
            config_dict["sampler"] = sampler

        if batch_count := data.get(
            "batch_count", data.get("batch_count", data.get("batchCount", None))
        ):
            config_dict["batch_count"] = batch_count

        if batch_size := data.get(
            "batch_size", data.get("batch_size", data.get("batchSize", None))
        ):
            config_dict["batch_size"] = batch_size

        if hires_fix := data.get("hires_fix", data.get("hires_fix", None)):
            config_dict["hires_fix"] = hires_fix

        if hires_fix_width := data.get(
            "hires_fix_width",
            data.get("hires_fix_start_width", data.get("hiresFixWidth", None)),
        ):
            config_dict["hires_fix_width"] = hires_fix_width

        if hires_fix_height := data.get(
            "hires_fix_height",
            data.get("hires_fix_start_height", data.get("hiresFixHeight", None)),
        ):
            config_dict["hires_fix_height"] = hires_fix_height

        if hires_fix_strength := data.get(
            "hires_fix_strength",
            data.get("hires_fix_strength", data.get("hiresFixStrength", None)),
        ):
            config_dict["hires_fix_strength"] = hires_fix_strength

        if upscaler := data.get("upscaler", data.get("upscaler", None)):
            config_dict["upscaler"] = upscaler

        if image_guidance_scale := data.get(
            "image_guidance_scale",
            data.get("image_guidance_scale", data.get("imageGuidanceScale", None)),
        ):
            config_dict["image_guidance_scale"] = image_guidance_scale

        if seed_mode := data.get(
            "seed_mode", data.get("seed_mode", data.get("seedMode", None))
        ):
            config_dict["seed_mode"] = seed_mode

        if clip_skip := data.get(
            "clip_skip", data.get("clip_skip", data.get("clipSkip", None))
        ):
            config_dict["clip_skip"] = clip_skip

        if mask_blur := data.get(
            "mask_blur", data.get("mask_blur", data.get("maskBlur", None))
        ):
            config_dict["mask_blur"] = mask_blur

        if face_restoration := data.get(
            "face_restoration",
            data.get("face_restoration", data.get("faceRestoration", None)),
        ):
            config_dict["face_restoration"] = face_restoration

        if decode_with_attention := data.get(
            "decode_with_attention",
            data.get("decode_with_attention", data.get("decodeWithAttention", None)),
        ):
            config_dict["decode_with_attention"] = decode_with_attention

        if hires_fix_decode_with_attention := data.get(
            "hires_fix_decode_with_attention",
            data.get(
                "hires_fix_decode_with_attention",
                data.get("hiresFixDecodeWithAttention", None),
            ),
        ):
            config_dict["hires_fix_decode_with_attention"] = (
                hires_fix_decode_with_attention
            )

        if clip_weight := data.get(
            "clip_weight", data.get("clip_weight", data.get("clipWeight", None))
        ):
            config_dict["clip_weight"] = clip_weight

        if negative_prompt_for_image_prior := data.get(
            "negative_prompt_for_image_prior",
            data.get(
                "negative_prompt_for_image_prior",
                data.get("negativePromptForImagePrior", None),
            ),
        ):
            config_dict["negative_prompt_for_image_prior"] = (
                negative_prompt_for_image_prior
            )

        if image_prior_steps := data.get(
            "image_prior_steps",
            data.get("image_prior_steps", data.get("imagePriorSteps", None)),
        ):
            config_dict["image_prior_steps"] = image_prior_steps

        if refiner_model := data.get(
            "refiner_model", data.get("refiner_model", data.get("refinerModel", None))
        ):
            config_dict["refiner_model"] = refiner_model

        if original_image_height := data.get(
            "original_image_height",
            data.get("original_image_height", data.get("originalImageHeight", None)),
        ):
            config_dict["original_image_height"] = original_image_height

        if original_image_width := data.get(
            "original_image_width",
            data.get("original_image_width", data.get("originalImageWidth", None)),
        ):
            config_dict["original_image_width"] = original_image_width

        if crop_top := data.get(
            "crop_top", data.get("crop_top", data.get("cropTop", None))
        ):
            config_dict["crop_top"] = crop_top

        if crop_left := data.get(
            "crop_left", data.get("crop_left", data.get("cropLeft", None))
        ):
            config_dict["crop_left"] = crop_left

        if target_image_height := data.get(
            "target_image_height",
            data.get("target_image_height", data.get("targetImageHeight", None)),
        ):
            config_dict["target_image_height"] = target_image_height

        if target_image_width := data.get(
            "target_image_width",
            data.get("target_image_width", data.get("targetImageWidth", None)),
        ):
            config_dict["target_image_width"] = target_image_width

        if aesthetic_score := data.get(
            "aesthetic_score",
            data.get("aesthetic_score", data.get("aestheticScore", None)),
        ):
            config_dict["aesthetic_score"] = aesthetic_score

        if negative_aesthetic_score := data.get(
            "negative_aesthetic_score",
            data.get(
                "negative_aesthetic_score", data.get("negativeAestheticScore", None)
            ),
        ):
            config_dict["negative_aesthetic_score"] = negative_aesthetic_score

        if zero_negative_prompt := data.get(
            "zero_negative_prompt",
            data.get("zero_negative_prompt", data.get("zeroNegativePrompt", None)),
        ):
            config_dict["zero_negative_prompt"] = zero_negative_prompt

        if refiner_start := data.get(
            "refiner_start", data.get("refiner_start", data.get("refinerStart", None))
        ):
            config_dict["refiner_start"] = refiner_start

        if negative_original_image_height := data.get(
            "negative_original_image_height",
            data.get(
                "negative_original_image_height",
                data.get("negativeOriginalImageHeight", None),
            ),
        ):
            config_dict["negative_original_image_height"] = (
                negative_original_image_height
            )

        if negative_original_image_width := data.get(
            "negative_original_image_width",
            data.get(
                "negative_original_image_width",
                data.get("negativeOriginalImageWidth", None),
            ),
        ):
            config_dict["negative_original_image_width"] = negative_original_image_width

        if name := data.get("name", data.get("name", None)):
            config_dict["name"] = name

        if fps := data.get("fps", data.get("fps_id", data.get("fpsId", None))):
            config_dict["fps"] = fps

        if motion_scale := data.get(
            "motion_scale", data.get("motion_bucket_id", data.get("motionScale", None))
        ):
            config_dict["motion_scale"] = motion_scale

        if guiding_frame_noise := data.get(
            "guiding_frame_noise",
            data.get("cond_aug", data.get("guidingFrameNoise", None)),
        ):
            config_dict["guiding_frame_noise"] = guiding_frame_noise

        if guiding_frame_guidance := data.get(
            "guiding_frame_guidance",
            data.get("start_frame_cfg", data.get("guidingFrameGuidance", None)),
        ):
            config_dict["guiding_frame_guidance"] = guiding_frame_guidance

        if num_frames := data.get(
            "num_frames", data.get("num_frames", data.get("numFrames", None))
        ):
            config_dict["num_frames"] = num_frames

        if mask_blur_outset := data.get(
            "mask_blur_outset",
            data.get("mask_blur_outset", data.get("maskBlurOutset", None)),
        ):
            config_dict["mask_blur_outset"] = mask_blur_outset

        if sharpness := data.get("sharpness", data.get("sharpness", None)):
            config_dict["sharpness"] = sharpness

        if shift := data.get("shift", data.get("shift", None)):
            config_dict["shift"] = shift

        if stage_2_steps := data.get(
            "stage_2_steps", data.get("stage_2_steps", data.get("stage2Steps", None))
        ):
            config_dict["stage_2_steps"] = stage_2_steps

        if stage_2_cfg := data.get(
            "stage_2_cfg", data.get("stage_2_cfg", data.get("stage2Cfg", None))
        ):
            config_dict["stage_2_cfg"] = stage_2_cfg

        if stage_2_shift := data.get(
            "stage_2_shift", data.get("stage_2_shift", data.get("stage2Shift", None))
        ):
            config_dict["stage_2_shift"] = stage_2_shift

        if tiled_decoding := data.get(
            "tiled_decoding",
            data.get("tiled_decoding", data.get("tiledDecoding", None)),
        ):
            config_dict["tiled_decoding"] = tiled_decoding

        if decoding_tile_width := data.get(
            "decoding_tile_width",
            data.get("decoding_tile_width", data.get("decodingTileWidth", None)),
        ):
            config_dict["decoding_tile_width"] = decoding_tile_width

        if decoding_tile_height := data.get(
            "decoding_tile_height",
            data.get("decoding_tile_height", data.get("decodingTileHeight", None)),
        ):
            config_dict["decoding_tile_height"] = decoding_tile_height

        if decoding_tile_overlap := data.get(
            "decoding_tile_overlap",
            data.get("decoding_tile_overlap", data.get("decodingTileOverlap", None)),
        ):
            config_dict["decoding_tile_overlap"] = decoding_tile_overlap

        if stochastic_sampling_gamma := data.get(
            "stochastic_sampling_gamma",
            data.get(
                "stochastic_sampling_gamma", data.get("stochasticSamplingGamma", None)
            ),
        ):
            config_dict["stochastic_sampling_gamma"] = stochastic_sampling_gamma

        if preserve_original_after_inpaint := data.get(
            "preserve_original_after_inpaint",
            data.get(
                "preserve_original_after_inpaint",
                data.get("preserveOriginalAfterInpaint", None),
            ),
        ):
            config_dict["preserve_original_after_inpaint"] = (
                preserve_original_after_inpaint
            )

        if tiled_diffusion := data.get(
            "tiled_diffusion",
            data.get("tiled_diffusion", data.get("tiledDiffusion", None)),
        ):
            config_dict["tiled_diffusion"] = tiled_diffusion

        if diffusion_tile_width := data.get(
            "diffusion_tile_width",
            data.get("diffusion_tile_width", data.get("diffusionTileWidth", None)),
        ):
            config_dict["diffusion_tile_width"] = diffusion_tile_width

        if diffusion_tile_height := data.get(
            "diffusion_tile_height",
            data.get("diffusion_tile_height", data.get("diffusionTileHeight", None)),
        ):
            config_dict["diffusion_tile_height"] = diffusion_tile_height

        if diffusion_tile_overlap := data.get(
            "diffusion_tile_overlap",
            data.get("diffusion_tile_overlap", data.get("diffusionTileOverlap", None)),
        ):
            config_dict["diffusion_tile_overlap"] = diffusion_tile_overlap

        if upscaler_scale_factor := data.get(
            "upscaler_scale_factor",
            data.get("upscaler_scale_factor", data.get("upscalerScaleFactor", None)),
        ):
            config_dict["upscaler_scale_factor"] = upscaler_scale_factor

        if t5_text_encoder := data.get(
            "t5_text_encoder",
            data.get("t5_text_encoder", data.get("t5TextEncoder", None)),
        ):
            config_dict["t5_text_encoder"] = t5_text_encoder

        if separate_clip_l := data.get(
            "separate_clip_l",
            data.get("separate_clip_l", data.get("separateClipL", None)),
        ):
            config_dict["separate_clip_l"] = separate_clip_l

        if clip_l_text := data.get(
            "clip_l_text", data.get("clip_l_text", data.get("clipLText", None))
        ):
            config_dict["clip_l_text"] = clip_l_text

        if separate_open_clip_g := data.get(
            "separate_open_clip_g",
            data.get("separate_open_clip_g", data.get("separateOpenClipG", None)),
        ):
            config_dict["separate_open_clip_g"] = separate_open_clip_g

        if open_clip_g_text := data.get(
            "open_clip_g_text",
            data.get("open_clip_g_text", data.get("openClipGText", None)),
        ):
            config_dict["open_clip_g_text"] = open_clip_g_text

        if speed_up_with_guidance_embed := data.get(
            "speed_up_with_guidance_embed",
            data.get(
                "speed_up_with_guidance_embed",
                data.get("speedUpWithGuidanceEmbed", None),
            ),
        ):
            config_dict["speed_up_with_guidance_embed"] = speed_up_with_guidance_embed

        if guidance_embed := data.get(
            "guidance_embed",
            data.get("guidance_embed", data.get("guidanceEmbed", None)),
        ):
            config_dict["guidance_embed"] = guidance_embed

        if resolution_dependent_shift := data.get(
            "resolution_dependent_shift",
            data.get(
                "resolution_dependent_shift", data.get("resolutionDependentShift", None)
            ),
        ):
            config_dict["resolution_dependent_shift"] = resolution_dependent_shift

        if tea_cache_start := data.get(
            "tea_cache_start",
            data.get("tea_cache_start", data.get("teaCacheStart", None)),
        ):
            config_dict["tea_cache_start"] = tea_cache_start

        if tea_cache_end := data.get(
            "tea_cache_end", data.get("tea_cache_end", data.get("teaCacheEnd", None))
        ):
            config_dict["tea_cache_end"] = tea_cache_end

        if tea_cache_threshold := data.get(
            "tea_cache_threshold",
            data.get("tea_cache_threshold", data.get("teaCacheThreshold", None)),
        ):
            config_dict["tea_cache_threshold"] = tea_cache_threshold

        if tea_cache := data.get(
            "tea_cache", data.get("tea_cache", data.get("teaCache", None))
        ):
            config_dict["tea_cache"] = tea_cache

        if separate_t5 := data.get(
            "separate_t5", data.get("separate_t5", data.get("separateT5", None))
        ):
            config_dict["separate_t5"] = separate_t5

        if t5_text := data.get(
            "t5_text", data.get("t5_text", data.get("t5Text", None))
        ):
            config_dict["t5_text"] = t5_text

        if tea_cache_max_skip_steps := data.get(
            "tea_cache_max_skip_steps",
            data.get(
                "tea_cache_max_skip_steps", data.get("teaCacheMaxSkipSteps", None)
            ),
        ):
            config_dict["tea_cache_max_skip_steps"] = tea_cache_max_skip_steps

        if causal_inference_enabled := data.get(
            "causal_inference_enabled",
            data.get(
                "causal_inference_enabled", data.get("causalInferenceEnabled", None)
            ),
        ):
            config_dict["causal_inference_enabled"] = causal_inference_enabled

        if causal_inference := data.get(
            "causal_inference",
            data.get("causal_inference", data.get("causalInference", None)),
        ):
            config_dict["causal_inference"] = causal_inference

        if causal_inference_pad := data.get(
            "causal_inference_pad",
            data.get("causal_inference_pad", data.get("causalInferencePad", None)),
        ):
            config_dict["causal_inference_pad"] = causal_inference_pad

        if cfg_zero_star := data.get(
            "cfg_zero_star", data.get("cfg_zero_star", data.get("cfgZeroStar", None))
        ):
            config_dict["cfg_zero_star"] = cfg_zero_star

        if cfg_zero_init_steps := data.get(
            "cfg_zero_init_steps",
            data.get("cfg_zero_init_steps", data.get("cfgZeroInitSteps", None)),
        ):
            config_dict["cfg_zero_init_steps"] = cfg_zero_init_steps

        if compression_artifacts := data.get(
            "compression_artifacts",
            data.get("compression_artifacts", data.get("compressionArtifacts", None)),
        ):
            config_dict["compression_artifacts"] = compression_artifacts

        if compression_artifacts_quality := data.get(
            "compression_artifacts_quality",
            data.get(
                "compression_artifacts_quality",
                data.get("compressionArtifactsQuality", None),
            ),
        ):
            config_dict["compression_artifacts_quality"] = compression_artifacts_quality

        return GenConfig(config_dict)
