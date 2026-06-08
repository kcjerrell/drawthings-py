from __future__ import annotations
import flatbuffers
from .types import UpscalerModel, CompressionMethod, SeedMode, SamplerType
from drawthings_py.configs.gen_config_base import GenConfigBase
from drawthings_py.generated.dt_grpc.config_generated import GenerationConfigurationT
from typing import Unpack, cast, Any
import json


class GenConfig(GenConfigBase):
    _data: ConfigDict

    def __init__(self, **kwargs: Unpack[ConfigDict]):
        super().__init__(**kwargs)
                

                                                                                                     
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
        return SamplerType(cast(int, self._data.get("sampler", SamplerType.DPMPP2MKarras)))
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
        return UpscalerModel(cast(str, self._data.get("upscaler", None))) if self._data.get("upscaler", None) is not None else None
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
        """clip_skip Used with model versions SD, SD2, SDXL and SDXL"""
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
        return CompressionMethod(cast(int, self._data.get("compression_artifacts", CompressionMethod.Disabled)))
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
    def from_json(cls, json_text: str | None = None, json_data: ConfigDict | None = None) -> GenConfig:
        data = json_data if json_data is not None else cast(dict[str, Any], json.loads(json_text or "{}"))  # pyright: ignore[reportExplicitAny]
        config_dict = ConfigDict()
        if id := data.get("id") or data.get("id"):
            config_dict["id"] = cast(int, id)
        if width := data.get("width") or data.get("start_width") or data.get("width") or data.get("startWidth"):
            config_dict["width"] = cast(int, width)
        if height := data.get("height") or data.get("start_height") or data.get("height") or data.get("startHeight"):
            config_dict["height"] = cast(int, height)
        if steps := data.get("steps") or data.get("steps"):
            config_dict["steps"] = cast(int, steps)
        if guidance := data.get("guidance") or data.get("guidance_scale") or data.get("guidanceScale"):
            config_dict["guidance"] = cast(float, guidance)
        if strength := data.get("strength") or data.get("strength"):
            config_dict["strength"] = cast(float, strength)
        if model := data.get("model") or data.get("model"):
            config_dict["model"] = cast(str | None, model)
        if sampler := data.get("sampler") or data.get("sampler"):
            config_dict["sampler"] = cast(SamplerType, sampler)
        if batch_count := data.get("batch_count") or data.get("batch_count") or data.get("batchCount"):
            config_dict["batch_count"] = cast(int, batch_count)
        if batch_size := data.get("batch_size") or data.get("batch_size") or data.get("batchSize"):
            config_dict["batch_size"] = cast(int, batch_size)
        if hires_fix := data.get("hires_fix") or data.get("hires_fix"):
            config_dict["hires_fix"] = cast(bool, hires_fix)
        if hires_fix_width := data.get("hires_fix_width") or data.get("hires_fix_start_width") or data.get("hiresFixWidth"):
            config_dict["hires_fix_width"] = cast(int, hires_fix_width)
        if hires_fix_height := data.get("hires_fix_height") or data.get("hires_fix_start_height") or data.get("hiresFixHeight"):
            config_dict["hires_fix_height"] = cast(int, hires_fix_height)
        if hires_fix_strength := data.get("hires_fix_strength") or data.get("hires_fix_strength") or data.get("hiresFixStrength"):
            config_dict["hires_fix_strength"] = cast(float, hires_fix_strength)
        if upscaler := data.get("upscaler") or data.get("upscaler"):
            config_dict["upscaler"] = cast(UpscalerModel | None, upscaler)
        if image_guidance_scale := data.get("image_guidance_scale") or data.get("image_guidance_scale") or data.get("imageGuidanceScale"):
            config_dict["image_guidance_scale"] = cast(float, image_guidance_scale)
        if seed_mode := data.get("seed_mode") or data.get("seed_mode") or data.get("seedMode"):
            config_dict["seed_mode"] = cast(SeedMode, seed_mode)
        if clip_skip := data.get("clip_skip") or data.get("clip_skip") or data.get("clipSkip"):
            config_dict["clip_skip"] = cast(int, clip_skip)
        if mask_blur := data.get("mask_blur") or data.get("mask_blur") or data.get("maskBlur"):
            config_dict["mask_blur"] = cast(float, mask_blur)
        if face_restoration := data.get("face_restoration") or data.get("face_restoration") or data.get("faceRestoration"):
            config_dict["face_restoration"] = cast(str | None, face_restoration)
        if decode_with_attention := data.get("decode_with_attention") or data.get("decode_with_attention") or data.get("decodeWithAttention"):
            config_dict["decode_with_attention"] = cast(bool, decode_with_attention)
        if hires_fix_decode_with_attention := data.get("hires_fix_decode_with_attention") or data.get("hires_fix_decode_with_attention") or data.get("hiresFixDecodeWithAttention"):
            config_dict["hires_fix_decode_with_attention"] = cast(bool, hires_fix_decode_with_attention)
        if clip_weight := data.get("clip_weight") or data.get("clip_weight") or data.get("clipWeight"):
            config_dict["clip_weight"] = cast(float, clip_weight)
        if negative_prompt_for_image_prior := data.get("negative_prompt_for_image_prior") or data.get("negative_prompt_for_image_prior") or data.get("negativePromptForImagePrior"):
            config_dict["negative_prompt_for_image_prior"] = cast(bool, negative_prompt_for_image_prior)
        if image_prior_steps := data.get("image_prior_steps") or data.get("image_prior_steps") or data.get("imagePriorSteps"):
            config_dict["image_prior_steps"] = cast(int, image_prior_steps)
        if refiner_model := data.get("refiner_model") or data.get("refiner_model") or data.get("refinerModel"):
            config_dict["refiner_model"] = cast(str | None, refiner_model)
        if original_image_height := data.get("original_image_height") or data.get("original_image_height") or data.get("originalImageHeight"):
            config_dict["original_image_height"] = cast(int, original_image_height)
        if original_image_width := data.get("original_image_width") or data.get("original_image_width") or data.get("originalImageWidth"):
            config_dict["original_image_width"] = cast(int, original_image_width)
        if crop_top := data.get("crop_top") or data.get("crop_top") or data.get("cropTop"):
            config_dict["crop_top"] = cast(int, crop_top)
        if crop_left := data.get("crop_left") or data.get("crop_left") or data.get("cropLeft"):
            config_dict["crop_left"] = cast(int, crop_left)
        if target_image_height := data.get("target_image_height") or data.get("target_image_height") or data.get("targetImageHeight"):
            config_dict["target_image_height"] = cast(int, target_image_height)
        if target_image_width := data.get("target_image_width") or data.get("target_image_width") or data.get("targetImageWidth"):
            config_dict["target_image_width"] = cast(int, target_image_width)
        if aesthetic_score := data.get("aesthetic_score") or data.get("aesthetic_score") or data.get("aestheticScore"):
            config_dict["aesthetic_score"] = cast(float, aesthetic_score)
        if negative_aesthetic_score := data.get("negative_aesthetic_score") or data.get("negative_aesthetic_score") or data.get("negativeAestheticScore"):
            config_dict["negative_aesthetic_score"] = cast(float, negative_aesthetic_score)
        if zero_negative_prompt := data.get("zero_negative_prompt") or data.get("zero_negative_prompt") or data.get("zeroNegativePrompt"):
            config_dict["zero_negative_prompt"] = cast(bool, zero_negative_prompt)
        if refiner_start := data.get("refiner_start") or data.get("refiner_start") or data.get("refinerStart"):
            config_dict["refiner_start"] = cast(float, refiner_start)
        if negative_original_image_height := data.get("negative_original_image_height") or data.get("negative_original_image_height") or data.get("negativeOriginalImageHeight"):
            config_dict["negative_original_image_height"] = cast(int, negative_original_image_height)
        if negative_original_image_width := data.get("negative_original_image_width") or data.get("negative_original_image_width") or data.get("negativeOriginalImageWidth"):
            config_dict["negative_original_image_width"] = cast(int, negative_original_image_width)
        if name := data.get("name") or data.get("name"):
            config_dict["name"] = cast(str | None, name)
        if fps := data.get("fps") or data.get("fps_id") or data.get("fpsId"):
            config_dict["fps"] = cast(int, fps)
        if motion_scale := data.get("motion_scale") or data.get("motion_bucket_id") or data.get("motionScale"):
            config_dict["motion_scale"] = cast(int, motion_scale)
        if guiding_frame_noise := data.get("guiding_frame_noise") or data.get("cond_aug") or data.get("guidingFrameNoise"):
            config_dict["guiding_frame_noise"] = cast(float, guiding_frame_noise)
        if guiding_frame_guidance := data.get("guiding_frame_guidance") or data.get("start_frame_cfg") or data.get("guidingFrameGuidance"):
            config_dict["guiding_frame_guidance"] = cast(float, guiding_frame_guidance)
        if num_frames := data.get("num_frames") or data.get("num_frames") or data.get("numFrames"):
            config_dict["num_frames"] = cast(int, num_frames)
        if mask_blur_outset := data.get("mask_blur_outset") or data.get("mask_blur_outset") or data.get("maskBlurOutset"):
            config_dict["mask_blur_outset"] = cast(int, mask_blur_outset)
        if sharpness := data.get("sharpness") or data.get("sharpness"):
            config_dict["sharpness"] = cast(float, sharpness)
        if shift := data.get("shift") or data.get("shift"):
            config_dict["shift"] = cast(float, shift)
        if stage_2_steps := data.get("stage_2_steps") or data.get("stage_2_steps") or data.get("stage2Steps"):
            config_dict["stage_2_steps"] = cast(int, stage_2_steps)
        if stage_2_cfg := data.get("stage_2_cfg") or data.get("stage_2_cfg") or data.get("stage2Cfg"):
            config_dict["stage_2_cfg"] = cast(float, stage_2_cfg)
        if stage_2_shift := data.get("stage_2_shift") or data.get("stage_2_shift") or data.get("stage2Shift"):
            config_dict["stage_2_shift"] = cast(float, stage_2_shift)
        if tiled_decoding := data.get("tiled_decoding") or data.get("tiled_decoding") or data.get("tiledDecoding"):
            config_dict["tiled_decoding"] = cast(bool, tiled_decoding)
        if decoding_tile_width := data.get("decoding_tile_width") or data.get("decoding_tile_width") or data.get("decodingTileWidth"):
            config_dict["decoding_tile_width"] = cast(int, decoding_tile_width)
        if decoding_tile_height := data.get("decoding_tile_height") or data.get("decoding_tile_height") or data.get("decodingTileHeight"):
            config_dict["decoding_tile_height"] = cast(int, decoding_tile_height)
        if decoding_tile_overlap := data.get("decoding_tile_overlap") or data.get("decoding_tile_overlap") or data.get("decodingTileOverlap"):
            config_dict["decoding_tile_overlap"] = cast(int, decoding_tile_overlap)
        if stochastic_sampling_gamma := data.get("stochastic_sampling_gamma") or data.get("stochastic_sampling_gamma") or data.get("stochasticSamplingGamma"):
            config_dict["stochastic_sampling_gamma"] = cast(float, stochastic_sampling_gamma)
        if preserve_original_after_inpaint := data.get("preserve_original_after_inpaint") or data.get("preserve_original_after_inpaint") or data.get("preserveOriginalAfterInpaint"):
            config_dict["preserve_original_after_inpaint"] = cast(bool, preserve_original_after_inpaint)
        if tiled_diffusion := data.get("tiled_diffusion") or data.get("tiled_diffusion") or data.get("tiledDiffusion"):
            config_dict["tiled_diffusion"] = cast(bool, tiled_diffusion)
        if diffusion_tile_width := data.get("diffusion_tile_width") or data.get("diffusion_tile_width") or data.get("diffusionTileWidth"):
            config_dict["diffusion_tile_width"] = cast(int, diffusion_tile_width)
        if diffusion_tile_height := data.get("diffusion_tile_height") or data.get("diffusion_tile_height") or data.get("diffusionTileHeight"):
            config_dict["diffusion_tile_height"] = cast(int, diffusion_tile_height)
        if diffusion_tile_overlap := data.get("diffusion_tile_overlap") or data.get("diffusion_tile_overlap") or data.get("diffusionTileOverlap"):
            config_dict["diffusion_tile_overlap"] = cast(int, diffusion_tile_overlap)
        if upscaler_scale_factor := data.get("upscaler_scale_factor") or data.get("upscaler_scale_factor") or data.get("upscalerScaleFactor"):
            config_dict["upscaler_scale_factor"] = cast(int, upscaler_scale_factor)
        if t5_text_encoder := data.get("t5_text_encoder") or data.get("t5_text_encoder") or data.get("t5TextEncoder"):
            config_dict["t5_text_encoder"] = cast(bool, t5_text_encoder)
        if separate_clip_l := data.get("separate_clip_l") or data.get("separate_clip_l") or data.get("separateClipL"):
            config_dict["separate_clip_l"] = cast(bool, separate_clip_l)
        if clip_l_text := data.get("clip_l_text") or data.get("clip_l_text") or data.get("clipLText"):
            config_dict["clip_l_text"] = cast(str | None, clip_l_text)
        if separate_open_clip_g := data.get("separate_open_clip_g") or data.get("separate_open_clip_g") or data.get("separateOpenClipG"):
            config_dict["separate_open_clip_g"] = cast(bool, separate_open_clip_g)
        if open_clip_g_text := data.get("open_clip_g_text") or data.get("open_clip_g_text") or data.get("openClipGText"):
            config_dict["open_clip_g_text"] = cast(str | None, open_clip_g_text)
        if speed_up_with_guidance_embed := data.get("speed_up_with_guidance_embed") or data.get("speed_up_with_guidance_embed") or data.get("speedUpWithGuidanceEmbed"):
            config_dict["speed_up_with_guidance_embed"] = cast(bool, speed_up_with_guidance_embed)
        if guidance_embed := data.get("guidance_embed") or data.get("guidance_embed") or data.get("guidanceEmbed"):
            config_dict["guidance_embed"] = cast(float, guidance_embed)
        if resolution_dependent_shift := data.get("resolution_dependent_shift") or data.get("resolution_dependent_shift") or data.get("resolutionDependentShift"):
            config_dict["resolution_dependent_shift"] = cast(bool, resolution_dependent_shift)
        if tea_cache_start := data.get("tea_cache_start") or data.get("tea_cache_start") or data.get("teaCacheStart"):
            config_dict["tea_cache_start"] = cast(int, tea_cache_start)
        if tea_cache_end := data.get("tea_cache_end") or data.get("tea_cache_end") or data.get("teaCacheEnd"):
            config_dict["tea_cache_end"] = cast(int, tea_cache_end)
        if tea_cache_threshold := data.get("tea_cache_threshold") or data.get("tea_cache_threshold") or data.get("teaCacheThreshold"):
            config_dict["tea_cache_threshold"] = cast(float, tea_cache_threshold)
        if tea_cache := data.get("tea_cache") or data.get("tea_cache") or data.get("teaCache"):
            config_dict["tea_cache"] = cast(bool, tea_cache)
        if separate_t5 := data.get("separate_t5") or data.get("separate_t5") or data.get("separateT5"):
            config_dict["separate_t5"] = cast(bool, separate_t5)
        if t5_text := data.get("t5_text") or data.get("t5_text") or data.get("t5Text"):
            config_dict["t5_text"] = cast(str | None, t5_text)
        if tea_cache_max_skip_steps := data.get("tea_cache_max_skip_steps") or data.get("tea_cache_max_skip_steps") or data.get("teaCacheMaxSkipSteps"):
            config_dict["tea_cache_max_skip_steps"] = cast(int, tea_cache_max_skip_steps)
        if causal_inference_enabled := data.get("causal_inference_enabled") or data.get("causal_inference_enabled") or data.get("causalInferenceEnabled"):
            config_dict["causal_inference_enabled"] = cast(bool, causal_inference_enabled)
        if causal_inference := data.get("causal_inference") or data.get("causal_inference") or data.get("causalInference"):
            config_dict["causal_inference"] = cast(int, causal_inference)
        if causal_inference_pad := data.get("causal_inference_pad") or data.get("causal_inference_pad") or data.get("causalInferencePad"):
            config_dict["causal_inference_pad"] = cast(int, causal_inference_pad)
        if cfg_zero_star := data.get("cfg_zero_star") or data.get("cfg_zero_star") or data.get("cfgZeroStar"):
            config_dict["cfg_zero_star"] = cast(bool, cfg_zero_star)
        if cfg_zero_init_steps := data.get("cfg_zero_init_steps") or data.get("cfg_zero_init_steps") or data.get("cfgZeroInitSteps"):
            config_dict["cfg_zero_init_steps"] = cast(int, cfg_zero_init_steps)
        if compression_artifacts := data.get("compression_artifacts") or data.get("compression_artifacts") or data.get("compressionArtifacts"):
            config_dict["compression_artifacts"] = cast(CompressionMethod, compression_artifacts)
        if compression_artifacts_quality := data.get("compression_artifacts_quality") or data.get("compression_artifacts_quality") or data.get("compressionArtifactsQuality"):
            config_dict["compression_artifacts_quality"] = cast(float, compression_artifacts_quality)
        config = GenConfig.from_dict(config_dict)
        GenConfigBase._apply_json(config, json_text=json_text, json_data=json_data)
        return config


    def to_fbs(self, seed: int | None = None) -> bytes:
        builder = flatbuffers.Builder(0)
        config_t = GenerationConfigurationT()
        config_t.startWidth = int(round(self.width / 64))
        config_t.startHeight = int(round(self.height / 64))
        config_t.steps = self.steps
        config_t.guidanceScale = self.guidance
        config_t.strength = self.strength
        config_t.model = self.model
        config_t.sampler = self.sampler
        config_t.batchSize = self.batch_size
        config_t.hiresFix = self.hires_fix
        if not ((False if self.hires_fix else True)):
            config_t.hiresFixStartWidth = int(round(self.hires_fix_width / 64))

        if not ((False if self.hires_fix else True)):
            config_t.hiresFixStartHeight = int(round(self.hires_fix_height / 64))

        if not ((False if self.hires_fix else True)):
            config_t.hiresFixStrength = self.hires_fix_strength

        config_t.upscaler = self.upscaler
        config_t.imageGuidanceScale = self.image_guidance_scale
        config_t.seedMode = self.seed_mode
        config_t.clipSkip = self.clip_skip
        config_t.maskBlur = self.mask_blur
        config_t.faceRestoration = self.face_restoration
        config_t.refinerModel = self.refiner_model
        config_t.originalImageHeight = int(round(self.original_image_height / 64))
        config_t.originalImageWidth = int(round(self.original_image_width / 64))
        config_t.cropTop = int(round(self.crop_top / 64))
        config_t.cropLeft = int(round(self.crop_left / 64))
        config_t.targetImageHeight = int(round(self.target_image_height / 64))
        config_t.targetImageWidth = int(round(self.target_image_width / 64))
        config_t.zeroNegativePrompt = self.zero_negative_prompt
        if not ((False if self.refiner_model else True)):
            config_t.refinerStart = self.refiner_start

        config_t.negativeOriginalImageHeight = int(round(self.negative_original_image_height / 64))
        config_t.negativeOriginalImageWidth = int(round(self.negative_original_image_width / 64))
        config_t.fpsId = self.fps
        config_t.motionBucketId = self.motion_scale
        config_t.condAug = self.guiding_frame_noise
        config_t.startFrameCfg = self.guiding_frame_guidance
        config_t.numFrames = self.num_frames
        config_t.maskBlurOutset = self.mask_blur_outset
        config_t.sharpness = self.sharpness
        config_t.shift = self.shift
        config_t.tiledDecoding = self.tiled_decoding
        if not ((False if self.tiled_decoding else True)):
            config_t.decodingTileWidth = int(round(self.decoding_tile_width / 64))

        if not ((False if self.tiled_decoding else True)):
            config_t.decodingTileHeight = int(round(self.decoding_tile_height / 64))

        if not ((False if self.tiled_decoding else True)):
            config_t.decodingTileOverlap = int(round(self.decoding_tile_overlap / 64))

        if not ((False if self.sampler in [SamplerType.TCD, SamplerType.TCDTrailing] else True)):
            config_t.stochasticSamplingGamma = self.stochastic_sampling_gamma

        config_t.preserveOriginalAfterInpaint = self.preserve_original_after_inpaint
        config_t.tiledDiffusion = self.tiled_diffusion
        if not ((False if self.tiled_diffusion else True)):
            config_t.diffusionTileWidth = int(round(self.diffusion_tile_width / 64))

        if not ((False if self.tiled_diffusion else True)):
            config_t.diffusionTileHeight = int(round(self.diffusion_tile_height / 64))

        if not ((False if self.tiled_diffusion else True)):
            config_t.diffusionTileOverlap = int(round(self.diffusion_tile_overlap / 64))

        if not ((False if self.upscaler else True)):
            config_t.upscalerScaleFactor = self.upscaler_scale_factor

        config_t.t5TextEncoder = self.t5_text_encoder
        config_t.separateClipL = self.separate_clip_l
        if not ((False if self.separate_clip_l else True)):
            config_t.clipLText = self.clip_l_text

        config_t.separateOpenClipG = self.separate_open_clip_g
        if not ((False if self.separate_open_clip_g else True)):
            config_t.openClipGText = self.open_clip_g_text

        config_t.speedUpWithGuidanceEmbed = self.speed_up_with_guidance_embed
        if not ((True if self.speed_up_with_guidance_embed else False)):
            config_t.guidanceEmbed = self.guidance_embed

        config_t.resolutionDependentShift = self.resolution_dependent_shift
        if not ((False if self.tea_cache else True)):
            config_t.teaCacheStart = self.tea_cache_start

        if not ((False if self.tea_cache else True)):
            config_t.teaCacheEnd = self.tea_cache_end

        if not ((False if self.tea_cache else True)):
            config_t.teaCacheThreshold = self.tea_cache_threshold

        config_t.teaCache = self.tea_cache
        config_t.separateT5 = self.separate_t5
        if not ((False if self.separate_t5 else True)):
            config_t.t5Text = self.t5_text

        if not ((False if self.tea_cache else True)):
            config_t.teaCacheMaxSkipSteps = self.tea_cache_max_skip_steps

        config_t.causalInferenceEnabled = self.causal_inference_enabled
        if not ((False if self.causal_inference_enabled else True)):
            config_t.causalInference = self.causal_inference

        if not ((False if self.causal_inference_enabled else True)):
            config_t.causalInferencePad = self.causal_inference_pad

        config_t.cfgZeroStar = self.cfg_zero_star
        if not ((False if self.cfg_zero_star else True)):
            config_t.cfgZeroInitSteps = self.cfg_zero_init_steps

        config_t.compressionArtifacts = self.compression_artifacts
        if not ((True if self.compression_artifacts == CompressionMethod.Disabled else False)):
            config_t.compressionArtifactsQuality = self.compression_artifacts_quality

        config = config_t.Pack(builder)
        builder.Finish(config)
        return bytes(builder.Output())
