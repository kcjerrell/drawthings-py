from drawthings_py.configs import enums


def _run_common_to_int_tests(values_list, to_int_fn):
    default = to_int_fn(None)
    # valid int
    assert to_int_fn(1) == 1
    # valid str
    assert to_int_fn(values_list[1]) == 1
    # incorrect case str
    assert to_int_fn(values_list[1].lower()) == 1
    # invalid str
    assert to_int_fn("not_a_value") == default
    # out of range int
    assert to_int_fn(len(values_list) + 10) == default
    # None
    assert to_int_fn(None) == default


def _run_common_from_value_tests(values_list, from_value_fn, to_int_fn):
    default_index = to_int_fn(None)
    # valid int
    assert from_value_fn(1) == values_list[1]
    # valid str
    assert from_value_fn(values_list[1]) == values_list[1]
    # incorrect case str
    assert from_value_fn(values_list[1].lower()) == values_list[1]
    # invalid str
    assert from_value_fn("not_a_value") == values_list[default_index]
    # out of range int
    assert from_value_fn(len(values_list) + 10) == values_list[default_index]
    # None
    assert from_value_fn(None) == values_list[default_index]


def test_sampler_type_enum():
    _run_common_to_int_tests(enums.SAMPLER_TYPE_VALUES, enums.sampler_type_to_int)
    _run_common_from_value_tests(
        enums.SAMPLER_TYPE_VALUES,
        enums.sampler_type_from_value,
        enums.sampler_type_to_int,
    )


def test_seed_mode_enum():
    _run_common_to_int_tests(enums.SEED_MODE_VALUES, enums.seed_mode_to_int)
    _run_common_from_value_tests(
        enums.SEED_MODE_VALUES, enums.seed_mode_from_value, enums.seed_mode_to_int
    )


def test_control_mode_enum():
    _run_common_to_int_tests(enums.CONTROL_MODE_VALUES, enums.control_mode_to_int)
    _run_common_from_value_tests(
        enums.CONTROL_MODE_VALUES,
        enums.control_mode_from_value,
        enums.control_mode_to_int,
    )


def test_control_input_type_enum():
    _run_common_to_int_tests(
        enums.CONTROL_INPUT_TYPE_VALUES, enums.control_input_type_to_int
    )
    _run_common_from_value_tests(
        enums.CONTROL_INPUT_TYPE_VALUES,
        enums.control_input_type_from_value,
        enums.control_input_type_to_int,
    )


def test_lora_mode_enum():
    _run_common_to_int_tests(enums.LORA_MODE_VALUES, enums.lora_mode_to_int)
    _run_common_from_value_tests(
        enums.LORA_MODE_VALUES, enums.lora_mode_from_value, enums.lora_mode_to_int
    )


def test_compression_method_enum():
    _run_common_to_int_tests(
        enums.COMPRESSION_METHOD_VALUES, enums.compression_method_to_int
    )
    _run_common_from_value_tests(
        enums.COMPRESSION_METHOD_VALUES,
        enums.compression_method_from_value,
        enums.compression_method_to_int,
    )
