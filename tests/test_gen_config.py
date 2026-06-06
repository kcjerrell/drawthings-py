import json
from drawthings_py.configs.gen_config_generated import GenConfig
from drawthings_py.configs.configs import Configs


def test_from_json():
    json_text = Configs.get_json("anima_preview_3")
    config = json.loads(json_text)

    gc = GenConfig.from_json(json.dumps(config))

    assert gc.batch_size == 1
    assert gc.clip_skip == 2
    assert gc.guidance == 4
    assert gc.height == 1024
    assert not gc.hires_fix
    assert gc.mask_blur == 2.5
    assert gc.mask_blur_outset == 0
    assert gc.model == "anima_preview_3_f16.ckpt"
    assert gc.resolution_dependent_shift
    assert gc.sampler.value == 16
    assert gc.seed_mode.value == 2
    assert not gc.separate_clip_l
    assert not gc.separate_open_clip_g
    assert gc.sharpness == 0
    assert gc.steps == 30
    assert gc.strength == 1
    assert not gc.tea_cache
    assert gc.t5_text_encoder
    assert not gc.tiled_decoding
    assert not gc.tiled_diffusion
    assert gc.upscaler_scale_factor == 0
    assert gc.width == 1024
    assert gc.tea_cache_threshold == 0.3
    assert gc.tea_cache_start == 5
    assert gc.tea_cache_end == -1
    assert gc.tea_cache_max_skip_steps == 3
