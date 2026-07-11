from drawthings_py import Configs, ConfigDict


def test_combine():
    a = ConfigDict(seed=5, model="hello")
    b = ConfigDict(seed=0, steps=15)
    c = ConfigDict(steps=20, guidance=5)

    combined = Configs.combine(a, b, c)
    assert combined.get("seed") == 5
    assert combined.get("model") == "hello"
    assert combined.get("steps") == 15
    assert combined.get("guidance") == 5


def test_create():
    # Test creation with keyword arguments
    c1 = Configs.create(width=1024, height=1024)
    assert c1.width == 1024
    assert c1.height == 1024

    # Test creation with dictionary argument
    c2 = Configs.create({"width": 768, "height": 768})
    assert c2.width == 768
    assert c2.height == 768
