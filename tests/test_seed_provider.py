from drawthings_py.seed_provider import SeedProvider


def test_seed_provider():
    sp = SeedProvider()

    # positive seeds are returned as-is
    assert 555 == sp.get_seed(555)

    # -1 is random every time
    assert sp.get_seed(-1) != sp.get_seed(-1)
    assert sp.get_seed(-1) != sp.get_seed(-1)
    assert sp.get_seed(-1) != sp.get_seed(-1)

    # Other negative numbers are reusable once generated
    seed_a = sp.get_seed(-2)
    seed_b = sp.get_seed(-999)

    assert seed_a == sp.get_seed(-2)
    assert seed_a == sp.get_seed(-2)
    assert seed_a == sp.get_seed(-2)

    assert seed_b == sp.get_seed(-999)
    assert seed_b == sp.get_seed(-999)
    assert seed_b == sp.get_seed(-999)


def seeds_are_reproducible():
    sp = SeedProvider("seed seed")

    seeds = [sp.get_seed(-1) for _ in range(10)]

    sp2 = SeedProvider("seed seed")
    seeds2 = [sp2.get_seed(-1) for _ in range(10)]

    assert seeds == seeds2
