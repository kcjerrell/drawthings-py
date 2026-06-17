from drawthings_py.configs._util import describe_config
from drawthings_py.configs.gen_config import GenConfig


def test_accepts_genconfig_and_dict() -> None:
    g = GenConfig()
    g["model"] = "flux_test.ckpt"
    res1 = describe_config(g)
    res2 = describe_config({"model": "flux_test.ckpt"})
    assert isinstance(res1, str)
    assert isinstance(res2, str)


def test_handles_missing_values() -> None:
    assert isinstance(describe_config({}), str)
    assert isinstance(describe_config(GenConfig()), str)


def test_handles_loras_shift_strength() -> None:
    cfg = {
        "loras": [{"file": "a.ckpt"}, {"file": "b.skpt"}],
        "resolution_dependent_shift": True,
        "strength": 1.0,
    }
    assert isinstance(describe_config(cfg), str)
