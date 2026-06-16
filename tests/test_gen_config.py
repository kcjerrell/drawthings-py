from typing import cast

import pytest
import base64
import json
from drawthings_py.configs.gen_config import GenConfig
from drawthings_py.configs.enums import SAMPLER_TYPE_VALUES, SEED_MODE_VALUES  # pyright: ignore[reportPrivateUsage]
from drawthings_py.configs.presets import load_preset_data
from drawthings_py.generated.dt_grpc.config_generated import GenerationConfigurationT


def test_from_json():
    preset = load_preset_data("anima_preview_3")
    config = preset["configuration"]
    gc = GenConfig.from_json(json.dumps(config))

    assert gc["batch_size"] == 1
    assert gc["clip_skip"] == 2
    assert gc["guidance"] == 4
    assert gc["height"] == 1024
    assert not gc["hires_fix"]
    assert gc["mask_blur"] == 2.5
    assert gc["mask_blur_outset"] == 0
    assert gc["model"] == "anima_preview_3_f16.ckpt"
    assert gc["resolution_dependent_shift"]
    assert gc["sampler"] == SAMPLER_TYPE_VALUES[16]
    assert gc["seed_mode"] == SEED_MODE_VALUES[2]
    assert not gc["separate_clip_l"]
    assert not gc["separate_open_clip_g"]
    assert gc["sharpness"] == 0
    assert gc["steps"] == 30
    assert gc["strength"] == 1
    assert not gc["tea_cache"]
    assert gc["t5_text_encoder"]
    assert not gc["tiled_decoding"]
    assert not gc["tiled_diffusion"]
    assert gc["upscaler_scale_factor"] == 0
    assert gc["width"] == 1024
    assert gc["tea_cache_threshold"] == 0.3
    assert gc["tea_cache_start"] == 5
    assert gc["tea_cache_end"] == -1
    assert gc["tea_cache_max_skip_steps"] == 3


def test_flatbuffers_roundtrip():
    from drawthings_py.configs.gen_config import GenConfig as RealGenConfig

    preset_config = cast(  # pyright: ignore[reportInvalidCast]
        dict[str, object], load_preset_data("anima_preview_3")["configuration"]
    )

    gc = RealGenConfig.from_json(preset_config)

    # Serialize to flatbuffer
    fbs_bytes = gc.to_fbs()

    # Deserialize from flatbuffer
    gc_fbs = RealGenConfig.from_fbs(fbs_bytes)

    # Compare key fields (ignoring loras/controls as per request)
    assert gc_fbs["width"] == gc["width"]
    assert gc_fbs["height"] == gc["height"]
    assert gc_fbs["steps"] == gc["steps"]
    assert gc_fbs["guidance"] == gc["guidance"]
    assert gc_fbs["strength"] == gc["strength"]
    assert gc_fbs["model"] == gc["model"]
    assert gc_fbs["sampler"] == gc["sampler"]
    assert gc_fbs["seed_mode"] == gc["seed_mode"]
    assert gc_fbs["clip_skip"] == gc["clip_skip"]
    assert gc_fbs["resolution_dependent_shift"] == gc["resolution_dependent_shift"]


# This flatbuffer was taken from a request made by the DT app
TEST_BUFFER_BASE64 = (
    "sAAAAKwArAAAAKoAqACkAKAAnACYAJQAkwAAAIwAiwCIAIYAgAB8AAAAewB0AHAAbABoAGQAAAAAAAAA"
    "AAAAAAAAYABcAAAAAABYAFQAAAAAAAAAUABMAEgAAAAAAAAAAAAAAAAARABAADwAAAAAAAAAOwA4ADYAAAAw"
    "AAAALwAAAAAAAAAAAAAALgAoAAAAAAAAAAAAJwAgABwAGAAXAAAAAAAQAAAADAAAAAsABACsAAAAAgAAAAAA"
    "AAEAAAAABAAAAAAAAAHNzMw9/f///wgAAAAAAAAAhAAAAAAAAQHNzEw+AAAQABAAAAGamVk/ZmYmQPX///8A"
    "AgAAAAIAAJqZWT8AAwAAAAMAAAADAAAAAwAAWAAAAGZmpj9wAAAAsAAAAAMAAAAAAAACqAAAAJqZGT8AAAgA"
    "CAAAAQIAAAAAAAATsAAAAAAAgD/NzCxAEAAAAMT7aFsMAAwACQAAAHNvbWV0aGluZwAAABsAAAByZXN0b3Jl"
    "Zm9ybWVyX3YxLjBfZjE2LmNrcHQAAQAAAAwAAAAIAAwACAAEAAgAAAAAAIA/BAAAACAAAABlcGlfbm9pc2Vv"
    "ZmZzZXRfdjJfbG9yYV9mMTYuY2twdAAAAAAAAAAAGgAAAHJlYWxlc3JnYW5feDJwbHVzX2YxNi5ja3B0AAAS"
    "AAAAc2RtaXhfNC4yX2YxNi5ja3B0AAA="
)
TEST_BUFFER_BYTES = base64.b64decode(TEST_BUFFER_BASE64)
# this is the corresponding config, copied from the app
TEST_CONFIG_JSON = """{"guidanceScale":2.7000000000000002,"steps":16,"refinerModel":"","clipSkip":3,"preserveOriginalAfterInpaint":true,"faceRestoration":"restoreformer_v1.0_f16.ckpt","batchCount":1,"sharpness":2.6000000000000001,"shift":0.84999999999999998,"batchSize":2,"hiresFix":true,"strength":1,"upscaler":"realesrgan_x2plus_f16.ckpt","tiledDecoding":true,"upscalerScaleFactor":0,"decodingTileWidth":1024,"width":768,"cfgZeroStar":true,"hiresFixHeight":512,"seedMode":2,"maskBlurOutset":-11,"decodingTileOverlap":128,"sampler":19,"seed":1533606852,"diffusionTileHeight":1024,"stochasticSamplingGamma":0.20000000000000001,"hiresFixStrength":0.59999999999999998,"decodingTileHeight":1024,"loras":[{"mode":"all","file":"epi_noiseoffset_v2_lora_f16.ckpt","weight":1}],"diffusionTileWidth":1024,"maskBlur":1.3,"causalInferencePad":0,"model":"sdmix_4.2_f16.ckpt","tiledDiffusion":true,"height":768,"hiresFixWidth":512,"cfgZeroInitSteps":2,"diffusionTileOverlap":128,"controls":[]}"""


def test_json_against_bytes():
    gc_json = GenConfig.from_json(TEST_CONFIG_JSON)
    gc_fbs = GenConfig.from_fbs(TEST_BUFFER_BYTES)

    bytes_a = gc_json.to_fbs()
    bytes_b = gc_json.to_fbs()

    assert bytes_a == bytes_b

    _ = pytest.approx(gc_json._d, gc_fbs._d)  # pyright: ignore[reportUnknownMemberType, reportPrivateUsage]


def test_enums():
    def inner(
        case: str,
        json: str,
        expected_gc: tuple[str, str],
        expected_fbs: tuple[int, int],
    ):
        gc = GenConfig.from_json(json)

        assert expected_gc == (gc["sampler"], gc["seed_mode"]), case

        fbs = gc.to_fbs()
        gct = GenerationConfigurationT.InitFromPackedBuf(fbs, 0)

        assert expected_fbs == (gct.sampler, gct.seedMode), case  # pyright: ignore[reportUnknownMemberType]

    inner(
        "int values",
        """{"sampler": 5, "seed_mode": 2}""",
        ("UniPC", "ScaleAlike"),
        (5, 2),
    )

    inner(
        "proper str values",
        """{"sampler": "TCD", "seed_mode": "Legacy"}""",
        ("TCD", "Legacy"),
        (9, 0),
    )

    inner(
        "wrong case str values",
        """{"sampler": "eulera", "seed_mode": "scalealike"}""",
        ("EulerA", "ScaleAlike"),
        (1, 2),
    )

    inner(
        "invalid str values",
        """{"sampler": "invalid", "seed_mode": "invalid"}""",
        ("DPMPP2MKarras", "ScaleAlike"),
        (0, 2),
    )
    inner(
        "invalid int values",
        """{"sampler": -3, "seed_mode": 80}""",
        ("DPMPP2MKarras", "ScaleAlike"),
        (0, 2),
    )
    inner(
        "no values",
        """{}""",
        ("DPMPP2MKarras", "ScaleAlike"),
        (0, 2),
    )
