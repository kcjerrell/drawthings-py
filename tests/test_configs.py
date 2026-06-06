from drawthings_py.configs.configs import Configs
from drawthings_py.configs.types import ConfigDict


def test_combine():
    a = ConfigDict(seed=5, model="hello")
    b = ConfigDict(seed=0, steps=15)
    c = ConfigDict(steps=20, guidance=5)

    combined = Configs.combine(a, b, c)
    assert combined.get("seed") == 5
    assert combined.get("model") == "hello"
    assert combined.get("steps") == 15
    assert combined.get("guidance") == 5
