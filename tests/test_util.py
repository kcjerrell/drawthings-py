from drawthings_py.util._util import seeds_from_batch


def test_seeds_from_batch_examples():
    # example 1
    init = 1000
    size = 4
    expected = [1000, 266172694, 3204629577, 385443340]
    assert seeds_from_batch(init, size, 2) == expected

    # example 2
    init = 99999999
    size = 4
    expected = [99999999, 2225200458, 1578146574, 3814640502]
    assert seeds_from_batch(init, size, 2) == expected

    init = 555
    size = 4
    expected = [555, 555, 555, 555]
    assert seeds_from_batch(init, size, 0) == expected
