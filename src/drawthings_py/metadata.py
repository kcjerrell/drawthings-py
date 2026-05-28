from enum import IntEnum
from typing import Any, List, Optional, TypedDict


class SeedMode(IntEnum):
	Legacy = 0
	TorchCpuCompatible = 1
	ScaleAlike = 2
	NvidiaGpuCompatible = 3


class Sampler(IntEnum):
	Unknown = -1
	DPMPP2MKarras = 0
	EulerA = 1
	DDIM = 2
	PLMS = 3
	DPMPPSDEKarras = 4
	UniPC = 5
	LCM = 6
	EulerASubstep = 7
	DPMPPSDESubstep = 8
	TCD = 9
	EulerATrailing = 10
	DPMPPSDETrailing = 11
	DPMPP2MAYS = 12
	EulerAAYS = 13
	DPMPPSDEAYS = 14
	DPMPP2MTrailing = 15
	DDIMTrailing = 16
	UniPCTrailing = 17
	UniPCAYS = 18
	TCDTrailing = 19


class V2(TypedDict):
	aesthetic_score: float
	batch_count: int
	batch_size: int
	causal_inference: int
	causal_inference_pad: int
	cfg_zero_init_steps: int
	cfg_zero_star: bool
	clip_l_text: Optional[str]
	clip_skip: int
	clip_weight: float
	controls: List[Any]
	crop_left: int
	crop_top: int
	decoding_tile_height: int
	decoding_tile_overlap: int
	decoding_tile_width: int
	diffusion_tile_height: int
	diffusion_tile_overlap: int
	diffusion_tile_width: int
	fps: int
	guidance_embed: float
	guidance_scale: float
	guiding_frame_noise: float
	height: int
	hires_fix: bool
	hires_fix_height: int
	hires_fix_strength: float
	hires_fix_width: int
	id: int
	image_guidance_scale: float
	image_prior_steps: int
	loras: List[Any]
	mask_blur: float
	mask_blur_outset: int
	model: str
	motion_scale: int
	negative_aesthetic_score: float
	negative_original_image_height: int
	negative_original_image_width: int
	negative_prompt_for_image_prior: bool
	num_frames: int
	original_image_height: int
	original_image_width: int
	preserve_original_after_inpaint: bool
	refiner_start: float
	resolution_dependent_shift: bool
	sampler: Sampler
	seed: int
	seed_mode: SeedMode
	separate_clip_l: bool
	separate_open_clip_g: bool
	separate_t5: bool
	sharpness: float
	shift: float
	speed_up_with_guidance_embed: bool
	stage2_guidance: float
	stage2_shift: float
	stage2_steps: int
	start_frame_guidance: float
	steps: int
	stochastic_sampling_gamma: float
	strength: float
	t5_text_encoder: bool
	target_image_height: int
	target_image_width: int
	tea_cache: bool
	tea_cache_end: int
	tea_cache_max_skip_steps: int
	tea_cache_start: int
	tea_cache_threshold: float
	tiled_decoding: bool
	tiled_diffusion: bool
	upscaler_scale_factor: int
	width: int
	zero_negative_prompt: bool
	refiner_model: Optional[str]
	upscaler: Optional[str]


class DrawThingsMetadata(TypedDict):
	c: str
	model: str
	profile: Optional[Any]
	sampler: Sampler
	scale: float
	seed: int
	seed_mode: SeedMode
	shift: float
	size: str
	steps: int
	strength: float
	uc: str
	v2: V2

