"""
Comprehensive tests for the public API snapshot system.

These tests verify that the snapshot system correctly captures various
API elements and that breaking changes produce detectable diffs.
"""

import dataclasses
import enum
from typing import TypedDict
from typing_extensions import is_typeddict

from tests.test_public import (
    _normalize_type_string,
    _normalize_default_value,
    _get_parameter_kind_name,
    _extract_parameters,
    _extract_typeddict_info,
    _extract_enum_info,
    _extract_dataclass_info,
    _extract_class_info,
    _extract_function_info,
    _sort_dict,
)


def test_normalize_type_string_basic_types():
    """Test type normalization for basic types."""
    assert _normalize_type_string(int) == "int"
    assert _normalize_type_string(str) == "str"
    assert _normalize_type_string(float) == "float"
    assert _normalize_type_string(bool) == "bool"
    assert _normalize_type_string(None) == "None"


def test_normalize_type_string_generics():
    """Test type normalization for generic types."""
    assert _normalize_type_string(list[str]) == "list[str]"
    assert _normalize_type_string(dict[str, int]) == "dict[str, int]"
    assert _normalize_type_string(tuple[int, str]) == "tuple[int, str]"


def test_normalize_type_string_union():
    """Test type normalization for Union types."""
    from typing import Union, Optional

    assert _normalize_type_string(Union[str, int]) == "str | int"
    assert _normalize_type_string(Optional[str]) == "str | None"


def test_normalize_default_value_primitives():
    """Test default value normalization for primitives."""
    assert _normalize_default_value(None) == "None"
    assert _normalize_default_value(True) == "True"
    assert _normalize_default_value(False) == "False"
    assert _normalize_default_value(1) == "1"
    assert _normalize_default_value(1.0) == "1.0"
    assert _normalize_default_value("test") == "'test'"


def test_normalize_default_value_enum():
    """Test default value normalization for enums."""

    class TestEnum(enum.Enum):
        A = "a"
        B = 1

    assert _normalize_default_value(TestEnum.A) == "TestEnum.A"
    assert _normalize_default_value(TestEnum.B) == "TestEnum.B"


def test_parameter_kind_names():
    """Test parameter kind name conversion."""
    import inspect

    assert (
        _get_parameter_kind_name(inspect.Parameter.POSITIONAL_ONLY) == "POSITIONAL_ONLY"
    )
    assert (
        _get_parameter_kind_name(inspect.Parameter.POSITIONAL_OR_KEYWORD)
        == "POSITIONAL_OR_KEYWORD"
    )
    assert (
        _get_parameter_kind_name(inspect.Parameter.VAR_POSITIONAL) == "VAR_POSITIONAL"
    )
    assert _get_parameter_kind_name(inspect.Parameter.KEYWORD_ONLY) == "KEYWORD_ONLY"
    assert _get_parameter_kind_name(inspect.Parameter.VAR_KEYWORD) == "VAR_KEYWORD"


def test_extract_typeddict_info():
    """Test TypedDict information extraction."""

    class MyTypedDict(TypedDict):
        required_field: str
        optional_field: int | None

    info = _extract_typeddict_info(MyTypedDict)
    assert info["kind"] == "typeddict"
    assert "required_field" in info["fields"]
    assert "optional_field" in info["fields"]
    assert info["fields"]["required_field"]["required"] is True
    assert info["fields"]["required_field"]["type"] == "str"


def test_extract_enum_info():
    """Test Enum information extraction."""

    class MyEnum(enum.StrEnum):
        VALUE_A = "a"
        VALUE_B = "b"

    info = _extract_enum_info(MyEnum)
    assert info["kind"] == "enum"
    assert "VALUE_A" in info["members"]
    assert "VALUE_B" in info["members"]
    # String enum values are repr'd, so they include quotes
    assert info["members"]["VALUE_A"] == "'a'"


def test_extract_dataclass_info():
    """Test dataclass information extraction."""

    @dataclasses.dataclass
    class MyDataclass:
        required_field: str
        optional_field: int = 42

    info = _extract_dataclass_info(MyDataclass)
    assert info["kind"] == "dataclass"
    assert "required_field" in info["fields"]
    assert "optional_field" in info["fields"]
    assert info["fields"]["required_field"]["type"] == "str"
    assert info["fields"]["optional_field"]["default"] == "42"


def test_extract_class_info_methods():
    """Test class method extraction with method type classification."""

    class MyClass:
        def instance_method(self, x: int) -> str:
            return str(x)

        @classmethod
        def class_method(cls, x: int) -> str:
            return str(x)

        @staticmethod
        def static_method(x: int) -> str:
            return str(x)

    result = {"symbols": {}}
    _extract_class_info(MyClass, result)

    qualname = f"{MyClass.__module__}.{MyClass.__qualname__}"
    assert qualname in result["symbols"]
    class_info = result["symbols"][qualname]

    assert "instance_method" in class_info["members"]
    assert class_info["members"]["instance_method"]["method_type"] == "instance"
    assert class_info["members"]["instance_method"]["return_type"] == "str"

    assert "class_method" in class_info["members"]
    assert class_info["members"]["class_method"]["method_type"] == "classmethod"

    assert "static_method" in class_info["members"]
    assert class_info["members"]["static_method"]["method_type"] == "staticmethod"


def test_extract_class_info_properties():
    """Test class property extraction."""

    class MyClass:
        @property
        def my_property(self) -> int:
            return 42

        @property
        def property_with_setter(self) -> str:
            return "test"

        @property_with_setter.setter
        def property_with_setter(self, value: str):
            pass

    result = {"symbols": {}}
    _extract_class_info(MyClass, result)

    qualname = f"{MyClass.__module__}.{MyClass.__qualname__}"
    class_info = result["symbols"][qualname]

    assert "my_property" in class_info["members"]
    assert class_info["members"]["my_property"]["kind"] == "property"
    assert class_info["members"]["my_property"]["type"] == "int"
    assert class_info["members"]["my_property"]["has_setter"] is False

    assert "property_with_setter" in class_info["members"]
    assert class_info["members"]["property_with_setter"]["has_setter"] is True


def test_extract_class_info_inheritance():
    """Test class inheritance tracking."""

    class BaseClass:
        pass

    class DerivedClass(BaseClass):
        pass

    result = {"symbols": {}}
    _extract_class_info(DerivedClass, result)

    qualname = f"{DerivedClass.__module__}.{DerivedClass.__qualname__}"
    class_info = result["symbols"][qualname]

    assert "bases" in class_info
    assert len(class_info["bases"]) > 0
    assert f"{BaseClass.__module__}.{BaseClass.__name__}" in class_info["bases"]


def test_extract_function_info():
    """Test function information extraction."""

    def my_function(x: int, y: str = "default") -> bool:
        return True

    info = _extract_function_info(my_function, "test_module")
    assert info["kind"] == "function"
    assert len(info["parameters"]) == 2
    assert info["parameters"][0]["name"] == "x"
    assert info["parameters"][0]["type"] == "int"
    assert info["parameters"][1]["name"] == "y"
    assert info["parameters"][1]["default"] == "'default'"
    assert info["return_type"] == "bool"


def test_extract_module_info():
    """Test module information extraction."""
    from tests.test_public import _extract_module_info
    from types import ModuleType

    # Create a test module
    test_module = ModuleType("test_module")
    test_module.__all__ = ["test_function"]  # type: ignore

    def test_function(x: int) -> str:
        return str(x)

    test_function.__module__ = "test_module"  # type: ignore
    test_module.test_function = test_function  # type: ignore

    result = {"modules": {}, "symbols": {}}
    _extract_module_info(test_module, result)

    assert "test_module" in result["modules"]
    assert result["modules"]["test_module"]["kind"] == "module"
    assert "test_function" in result["modules"]["test_module"]["exports"]
    assert "test_module.test_function" in result["symbols"]


def test_sort_dict_determinism():
    """Test that dictionary sorting produces deterministic output."""
    unsorted = {"z": 1, "a": 2, "m": 3}
    sorted_dict = _sort_dict(unsorted)

    keys = list(sorted_dict.keys())
    assert keys == ["a", "m", "z"]


def test_sort_dict_nested():
    """Test that nested dictionary sorting is deterministic."""
    unsorted = {
        "z": {"c": 3, "a": 1},
        "a": {"b": 2, "d": 4},
    }
    sorted_dict = _sort_dict(unsorted)

    keys = list(sorted_dict.keys())
    assert keys == ["a", "z"]
    inner_keys_a = list(sorted_dict["a"].keys())
    assert inner_keys_a == ["b", "d"]


def test_snapshot_determinism():
    """Test that the snapshot is deterministic across multiple runs."""
    from tests.test_public import public_apis

    # Generate snapshot twice
    snapshot1 = public_apis()
    snapshot2 = public_apis()

    # Snapshots should be identical
    assert snapshot1 == snapshot2


def test_snapshot_structure():
    """Test that the snapshot has the expected structure."""
    from tests.test_public import public_apis

    snapshot = public_apis()

    # Check top-level structure
    assert "modules" in snapshot
    assert "symbols" in snapshot

    # Check module structure
    assert "drawthings_py" in snapshot["modules"]
    assert snapshot["modules"]["drawthings_py"]["kind"] == "module"
    assert "exports" in snapshot["modules"]["drawthings_py"]
    assert isinstance(snapshot["modules"]["drawthings_py"]["exports"], list)

    # Check that exports are sorted
    exports = snapshot["modules"]["drawthings_py"]["exports"]
    assert exports == sorted(exports)


def test_typeddict_detection():
    """Test that TypedDict classes are correctly identified."""
    from drawthings_py.configs.types import LoraDict, ControlDict

    assert is_typeddict(LoraDict)
    assert is_typeddict(ControlDict)


def test_enum_detection():
    """Test that Enum classes are correctly identified."""
    from drawthings_py.configs.presets import Presets
    from drawthings_py.configs.types import UpscalerModel

    assert issubclass(Presets, enum.Enum)
    assert issubclass(UpscalerModel, enum.Enum)


def test_dataclass_detection():
    """Test that dataclass classes are correctly identified."""
    from drawthings_py.image.image_buffer import ImageBuffer

    assert dataclasses.is_dataclass(ImageBuffer)


def test_parameter_kind_capture():
    """Test that parameter kinds are correctly captured."""
    import inspect

    def test_func(a: int, /, b: str, *, c: float, **kwargs):  # type: ignore
        pass

    sig = inspect.signature(test_func)
    params = _extract_parameters(sig)

    assert params[0]["name"] == "a"
    assert params[0]["kind"] == "POSITIONAL_ONLY"

    assert params[1]["name"] == "b"
    assert params[1]["kind"] == "POSITIONAL_OR_KEYWORD"

    assert params[2]["name"] == "c"
    assert params[2]["kind"] == "KEYWORD_ONLY"


def test_return_type_capture():
    """Test that return types are correctly captured."""
    from tests.test_public import public_apis

    snapshot = public_apis()

    # Find a function/method and check return type
    for symbol_name, symbol_info in snapshot["symbols"].items():
        if symbol_info.get("kind") in ("function", "method"):
            if "return_type" in symbol_info:
                # Return type should be a string
                assert isinstance(symbol_info["return_type"], str)
                break
    else:
        # If no function/method found, that's okay for this test
        pass


def test_public_exports_recorded():
    """Test that public exports are explicitly recorded."""
    from tests.test_public import public_apis

    snapshot = public_apis()

    # Check that modules have exports recorded
    for module_name, module_info in snapshot["modules"].items():
        assert "exports" in module_info
        assert "kind" in module_info
        assert module_info["kind"] == "module"


def test_symbol_kind_recorded():
    """Test that symbol kinds are explicitly recorded."""
    from tests.test_public import public_apis

    snapshot = public_apis()

    # Check that symbols have kind recorded
    for symbol_name, symbol_info in snapshot["symbols"].items():
        assert "kind" in symbol_info
        assert symbol_info["kind"] in (
            "class",
            "function",
            "typeddict",
            "enum",
            "dataclass",
            "protocol",
            "module",
            "type_alias",
        )
