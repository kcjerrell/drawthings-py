from __future__ import annotations
from collections.abc import MutableMapping, Iterator
from typing import Unpack, overload, Literal, cast
from typing_extensions import override
import json
import flatbuffers  # pyright: ignore[reportMissingTypeStubs]
from drawthings_py.configs.config_dict import ConfigDict, ConfigKey, ConfigValue
from drawthings_py.configs.config_prop import load_props
from drawthings_py.generated.dt_grpc.config_generated import GenerationConfigurationT
from drawthings_py.configs.types import (
    CompressionMethod,
    ControlDict,
    LoraDict,
    LoraMode,
    SamplerType,
    SeedMode,
    UpscalerModel,
    control_dict_from_json,
)


CONFIG_PROPS = load_props()

GenConfigIntKey = Literal[
    "id",
    "width",
    "height",
    "seed",
    "steps",
    "batch_count",
    "batch_size",
    "hires_fix_width",
    "hires_fix_height",
    "clip_skip",
    "image_prior_steps",
    "original_image_height",
    "original_image_width",
    "crop_top",
    "crop_left",
    "target_image_height",
    "target_image_width",
    "negative_original_image_height",
    "negative_original_image_width",
    "fps",
    "motion_scale",
    "num_frames",
    "mask_blur_outset",
    "stage_2_steps",
    "decoding_tile_width",
    "decoding_tile_height",
    "decoding_tile_overlap",
    "diffusion_tile_width",
    "diffusion_tile_height",
    "diffusion_tile_overlap",
    "upscaler_scale_factor",
    "tea_cache_start",
    "tea_cache_end",
    "tea_cache_max_skip_steps",
    "causal_inference",
    "causal_inference_pad",
    "cfg_zero_init_steps",
]
GenConfigFloatKey = Literal[
    "guidance",
    "strength",
    "hires_fix_strength",
    "image_guidance_scale",
    "mask_blur",
    "clip_weight",
    "aesthetic_score",
    "negative_aesthetic_score",
    "refiner_start",
    "guiding_frame_noise",
    "guiding_frame_guidance",
    "sharpness",
    "shift",
    "stage_2_cfg",
    "stage_2_shift",
    "stochastic_sampling_gamma",
    "guidance_embed",
    "tea_cache_threshold",
    "compression_artifacts_quality",
]
GenConfigStrKey = Literal[
    "model",
    "face_restoration",
    "refiner_model",
    "name",
    "clip_l_text",
    "open_clip_g_text",
    "t5_text",
]
GenConfigBoolKey = Literal[
    "hires_fix",
    "decode_with_attention",
    "hires_fix_decode_with_attention",
    "negative_prompt_for_image_prior",
    "zero_negative_prompt",
    "tiled_decoding",
    "preserve_original_after_inpaint",
    "tiled_diffusion",
    "t5_text_encoder",
    "separate_clip_l",
    "separate_open_clip_g",
    "speed_up_with_guidance_embed",
    "resolution_dependent_shift",
    "tea_cache",
    "separate_t5",
    "causal_inference_enabled",
    "cfg_zero_star",
]


class GenConfig(MutableMapping[ConfigKey, ConfigValue]):
    _d: ConfigDict

    def __init__(self, **kwargs: Unpack[ConfigDict]):
        self._d = ConfigDict(**kwargs)

    @overload  # type: ignore
    def __setitem__(self, key: GenConfigIntKey, value: int) -> None: ...
    @overload
    def __setitem__(self, key: GenConfigFloatKey, value: float) -> None: ...
    @overload
    def __setitem__(self, key: GenConfigStrKey, value: str | None) -> None: ...
    @overload
    def __setitem__(self, key: Literal["sampler"], value: SamplerType) -> None: ...
    @overload
    def __setitem__(self, key: Literal["loras"], value: list[LoraDict]) -> None: ...
    @overload
    def __setitem__(
        self, key: Literal["controls"], value: list[ControlDict]
    ) -> None: ...
    @overload
    def __setitem__(self, key: GenConfigBoolKey, value: bool) -> None: ...
    @overload
    def __setitem__(
        self, key: Literal["upscaler"], value: UpscalerModel | None
    ) -> None: ...
    @overload
    def __setitem__(self, key: Literal["seed_mode"], value: SeedMode) -> None: ...
    @overload
    def __setitem__(
        self, key: Literal["compression_artifacts"], value: CompressionMethod
    ) -> None: ...
    @override
    def __setitem__(self, key: ConfigKey, value: ConfigValue) -> None:  # type: ignore[override]
        self._d[key] = value  # pyright: ignore[reportGeneralTypeIssues]

    @override
    def __delitem__(self, key: ConfigKey) -> None:
        if key in self._d:
            del self._d[key]

    @override
    def __iter__(self) -> Iterator[ConfigKey]:
        return cast(Iterator[ConfigKey], iter(self._d))

    @override
    def __len__(self) -> int:
        return len(self._d)

    @overload  # type: ignore
    def __getitem__(self, key: GenConfigIntKey) -> int: ...
    @overload
    def __getitem__(self, key: GenConfigFloatKey) -> float: ...
    @overload
    def __getitem__(self, key: GenConfigStrKey) -> str | None: ...
    @overload
    def __getitem__(self, key: Literal["sampler"]) -> SamplerType: ...
    @overload
    def __getitem__(self, key: Literal["loras"]) -> list[LoraDict]: ...
    @overload
    def __getitem__(self, key: Literal["controls"]) -> list[ControlDict]: ...
    @overload
    def __getitem__(self, key: GenConfigBoolKey) -> bool: ...
    @overload
    def __getitem__(self, key: Literal["upscaler"]) -> UpscalerModel | None: ...
    @overload
    def __getitem__(self, key: Literal["seed_mode"]) -> SeedMode: ...
    @overload
    def __getitem__(
        self, key: Literal["compression_artifacts"]
    ) -> CompressionMethod: ...
    @override
    def __getitem__(self, key: ConfigKey) -> ConfigValue:  # type: ignore[override]
        if self._d.get(key) is None:
            self._d[key] = CONFIG_PROPS[key].default  # pyright: ignore[reportGeneralTypeIssues]
        return self._d.get(key)

    def set(self, config: ConfigDict | None = None, /, **kwargs: Unpack[ConfigDict]):
        """
        Set configuration values.

        config.set({
            "width": 1024,
            "height": 1024,
        })

        config.set(height=1024, width=1024)

        Args:
            config: A dictionary of configuration values to set.
            **kwargs: Keyword arguments of configuration values to set.
        """
        self._d.update(config or kwargs)

    @overload
    def set_hires_fix(self, value: None, /) -> None: ...
    @overload
    def set_hires_fix(
        self, width: int, height: int, strength: float = 0.7, /
    ) -> None: ...
    def set_hires_fix(
        self,
        arg1: None | int = None,
        height: int | None = None,
        strength: float | None = 0.7,
        /,
    ) -> None:
        if arg1 is None:
            self["hires_fix"] = False
            del self["hires_fix_width"]
            del self["hires_fix_height"]
            del self["hires_fix_strength"]
        elif height is not None:
            self["hires_fix"] = True
            self["hires_fix_width"] = arg1
            self["hires_fix_height"] = height
            self["hires_fix_strength"] = strength if strength is not None else 0.7
        else:
            raise ValueError(
                "Invalid arguments for set_hires_fix. Either provide no arguments to disable, or width, height, and optionally strength to enable."
            )

    def add_lora(self, file: str, weight: float = 1.0, mode: LoraMode = LoraMode.All):
        """Add a LoRA to the configuration."""
        # checking for existence is not necessaary - __getitem__ assigns the default
        self["loras"].append({"file": file, "weight": weight, "mode": mode})

    @overload
    def add_control(self, json_str: str, /) -> None: ...
    @overload
    def add_control(self, control_dict: ControlDict, /) -> None: ...
    @overload
    def add_control(self, /, **kwargs: Unpack[ControlDict]) -> None: ...
    def add_control(
        self, arg: str | ControlDict | None = None, /, **kwargs: Unpack[ControlDict]
    ):
        """Add a control to the configuration."""
        # checking for existence is not necessaary - __getitem__ assigns the default
        if isinstance(arg, str):
            control = control_dict_from_json(arg)
        elif isinstance(arg, dict):
            control = arg
        else:
            control = kwargs

        self["controls"].append(cast(ControlDict, control))

    @property
    def width(self) -> int:
        """Width of the image in pixels (will be rounded to the nearest 64)"""
        return self._d.get("width", 0)

    @width.setter
    def width(self, value: int):
        self._d["width"] = value

    @property
    def height(self) -> int:
        """Height of the image in pixels (will be rounded to the nearest 64)"""
        return self._d.get("height", 0)

    @height.setter
    def height(self, value: int):
        self._d["height"] = value

    @property
    def seed(self) -> int:
        """controls the random number generation for the diffusion process, enabling reproducible image outputs when the same seed is used with identical parameters"""
        return self._d.get("seed", -1)

    @seed.setter
    def seed(self, value: int):
        self._d["seed"] = value

    @property
    def steps(self) -> int:
        """specifies the number of sampling iterations (denoising steps) performed during the image generation process"""
        return self._d.get("steps", 0)

    @steps.setter
    def steps(self, value: int):
        self._d["steps"] = value

    @property
    def guidance(self) -> float:
        """controls how strongly the generation follows the text prompt (also called CFG or text guidance)"""
        return self._d.get("guidance", 4.5)

    @guidance.setter
    def guidance(self, value: float):
        self._d["guidance"] = value

    @property
    def strength(self) -> float:
        """determines the denoising strength for img2img operations"""
        return self._d.get("strength", 0.0)

    @strength.setter
    def strength(self, value: float):
        self._d["strength"] = value

    @property
    def model(self) -> str | None:
        """specifies which model file to use for generation"""
        return self._d.get("model", None)

    @model.setter
    def model(self, value: str | None):
        self._d["model"] = value

    @property
    def sampler(self) -> SamplerType:
        """specifies the sampling algorithm and schedule to use for generation"""
        return self._d.get("sampler", "DPMPP2MKarras")

    @sampler.setter
    def sampler(self, value: SamplerType):
        self._d["sampler"] = value

    @property
    def loras(self) -> list[LoraDict]:
        """array of LoRA objects specifying LoRA models to apply during image generation"""
        return self._d.get("loras", [])

    @loras.setter
    def loras(self, value: list[LoraDict]):
        self._d["loras"] = value

    @property
    def controls(self) -> list[ControlDict]:
        """array of control objects specifying control models to apply during image generation"""
        return self._d.get("controls", [])

    @controls.setter
    def controls(self, value: list[ControlDict]):
        self._d["controls"] = value

    @property
    def shift(self) -> float:
        """applies a general transformation or offset during image generation"""
        return self._d.get("shift", 1.0)

    @shift.setter
    def shift(self, value: float):
        self._d["shift"] = value

    @property
    def resolution_dependent_shift(self) -> bool:
        """controls whether shift adjustments should be resolution-dependent during image generation. Used with model versions Flux.1, Flux.2, Flux.2 Klein 4b, Flux.2 Klein 9b, HiDream, Qwen, SD3, SD3 Large, Z Image and Cosmos2.5"""
        return self._d.get("resolution_dependent_shift", True)

    @resolution_dependent_shift.setter
    def resolution_dependent_shift(self, value: bool):
        self._d["resolution_dependent_shift"] = value

    def to_fbs(self, seed: int | None = None) -> bytes:
        builder = flatbuffers.Builder(0)
        config_t = GenerationConfigurationT()

        for prop in CONFIG_PROPS.values():
            prop.to_fbs(self._d, config_t, seed if prop.name == "seed" else None)

        fbs_config = config_t.Pack(builder)  # type: ignore[func-returns-value]
        builder.Finish(fbs_config)  # pyright: ignore[reportUnknownMemberType, reportUnusedCallResult]
        return bytes(builder.Output())

    @classmethod
    def from_json(cls, json_str: str) -> GenConfig:
        data = cast(dict[str, object], json.loads(json_str))
        config = ConfigDict()
        for prop in CONFIG_PROPS.values():
            if value := prop.from_json(data):
                config[prop.name] = value  # pyright: ignore[reportGeneralTypeIssues]
        return cls(**config)

    @classmethod
    def from_fbs(cls, data: bytes) -> GenConfig:
        config_t = GenerationConfigurationT.InitFromPackedBuf(data)
        config = ConfigDict()
        for prop in CONFIG_PROPS.values():
            value = prop.from_fbs(config_t)
            if value is not None:
                config[prop.name] = value  # pyright: ignore[reportGeneralTypeIssues]
        return cls(**config)
