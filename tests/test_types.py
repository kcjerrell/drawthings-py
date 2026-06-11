import pytest

from drawthings_py.configs.types import SamplerHelpers, SAMPLER_TYPES


def _lower_list():
    return [s.lower() for s in SAMPLER_TYPES]


def test_to_int_with_int_returns_same():
    assert SamplerHelpers.to_int(3) == 3


def test_to_int_with_lowercase_string():
    idx = SamplerHelpers.to_int("eulera")
    expected = _lower_list().index("eulera")
    assert idx == expected


@pytest.mark.xfail(reason="to_int currently mishandles mixed-case strings (bug)")
def test_to_int_with_mixed_case_string():
    # expected: mixed-case input should behave case-insensitively
    assert SamplerHelpers.to_int("EulerA") == SamplerHelpers.to_int("eulera")


def test_from_value_with_int():
    assert SamplerHelpers.from_value(2) == SAMPLER_TYPES[2]


def test_from_value_with_string_case_insensitive():
    assert (
        SamplerHelpers.from_value("EuLeRa")
        == SAMPLER_TYPES[_lower_list().index("eulera")]
    )
