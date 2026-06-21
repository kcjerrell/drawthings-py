"""
Public API snapshot test.

This module captures a comprehensive snapshot of the public API surface to detect
breaking changes between releases.

Limitations
-----------
The following API changes cannot be reliably detected by this snapshot:

1. **Behavioral changes**: Changes in the runtime behavior of functions/methods that
   maintain the same signature.
2. **Semantic contract changes**: Changes in undocumented behavior or assumptions
   about how functions should be used.
3. **Raised exception types**: Changes in which exceptions are raised or under what
   conditions (not captured in the snapshot).
4. **Runtime side effects**: Changes in side effects like logging, I/O, or state
   mutations.
5. **Performance regressions**: Changes in performance characteristics.
6. **Default value behavior**: While default values are serialized, complex objects
   may not be fully captured.
7. **Protocol implementation compliance**: Whether a class actually implements a
   Protocol correctly (only captures the declared interface).
"""

import dataclasses
import enum
import inspect
import json
from pathlib import Path
from typing import (
    Any,
    ForwardRef,
    get_args,
    get_origin,
    get_type_hints,
    Union,
)  # type: ignore
from typing_extensions import is_typeddict, Protocol, get_protocol_members

import drawthings_py
import drawthings_py.configs
import drawthings_py.drawthings


# Sentinel value for missing defaults
_NO_DEFAULT = object()


def _normalize_type_string(type_hint: Any) -> str:  # type: ignore
    """Convert a type hint to a stable string representation.

    This function normalizes type hints to produce consistent, stable output
    across runs and Python versions where practical.

    Args:
        type_hint: A type hint from annotations.

    Returns:
        A normalized string representation of the type.
    """
    if type_hint is None:
        return "None"
    if type_hint is inspect.Parameter.empty:
        return "__no_annotation__"
    if type_hint is _NO_DEFAULT:
        return "__no_default__"

    origin = get_origin(type_hint)
    args = get_args(type_hint)

    # Handle NoneType
    if type_hint is type(None):
        return "None"

    # Handle basic types
    if origin is None:
        if isinstance(type_hint, type):
            return type_hint.__name__
        if isinstance(type_hint, ForwardRef):
            return type_hint.__forward_arg__
        if isinstance(type_hint, str):
            return type_hint
        # Fallback for other objects
        return str(type_hint)

    # Handle Union types (including Optional)
    if origin is Union:
        normalized_args = [_normalize_type_string(arg) for arg in args]
        # Normalize Optional[X] to X | None
        if len(args) == 2 and type(None) in args:
            non_none_arg = args[0] if args[1] is type(None) else args[1]
            return f"{_normalize_type_string(non_none_arg)} | None"
        return " | ".join(normalized_args)

    # Handle generic types
    origin_name = _normalize_type_string(origin)
    if args:
        normalized_args = [_normalize_type_string(arg) for arg in args]
        # Sort args for determinism (e.g., dict keys)
        if origin_name in ("dict", "Dict"):
            if len(normalized_args) == 2:
                return f"dict[{normalized_args[0]}, {normalized_args[1]}]"
        return f"{origin_name}[{', '.join(normalized_args)}]"
    return origin_name


def _normalize_default_value(value: Any) -> str:  # type: ignore
    """Convert a default value to a stable string representation.

    This function serializes default values in a deterministic way, avoiding
    memory addresses and unstable representations.

    Args:
        value: A default value from a parameter or attribute.

    Returns:
        A normalized string representation of the value.
    """
    if value is _NO_DEFAULT:
        return "__no_default__"
    if value is None:
        return "None"
    if value is True:
        return "True"
    if value is False:
        return "False"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        return repr(value)
    if isinstance(value, enum.Enum):
        return f"{value.__class__.__name__}.{value.name}"
    if isinstance(value, (list, tuple, set, frozenset)):
        # For collections, try to serialize elements
        try:
            elements = [_normalize_default_value(v) for v in value]
            if isinstance(value, tuple):
                return f"({', '.join(elements)})"
            return f"[{', '.join(elements)}]"
        except Exception:
            pass

    # For unsupported objects, emit a stable placeholder
    return f"<{value.__class__.__name__}>"


def _get_parameter_kind_name(kind: Any) -> str:  # type: ignore
    """Convert a Parameter kind to its string name."""
    kind_names = {
        inspect.Parameter.POSITIONAL_ONLY: "POSITIONAL_ONLY",
        inspect.Parameter.POSITIONAL_OR_KEYWORD: "POSITIONAL_OR_KEYWORD",
        inspect.Parameter.VAR_POSITIONAL: "VAR_POSITIONAL",
        inspect.Parameter.KEYWORD_ONLY: "KEYWORD_ONLY",
        inspect.Parameter.VAR_KEYWORD: "VAR_KEYWORD",
    }
    return kind_names.get(kind, "UNKNOWN")


def _should_ignore(name: str, module_name: str) -> bool:
    """Check if a member should be ignored based on the rules."""
    if name.startswith("_"):
        return True
    if "generated" in module_name:
        return True
    if module_name.startswith("_"):
        return True
    return False


def _extract_referenced_types(type_hint: Any) -> set[type]:  # type: ignore
    """Extract all class types referenced in a type hint.

    This function recursively extracts all class types from a type hint,
    including types nested in generics like list[MyClass], dict[str, MyClass], etc.

    Args:
        type_hint: A type hint from annotations.

    Returns:
        A set of class types referenced in the type hint.
    """
    referenced = set()

    if (
        type_hint is None
        or type_hint is inspect.Parameter.empty
        or type_hint is _NO_DEFAULT
    ):
        return referenced

    # Import os to check for PathLike
    import os

    # Handle basic types that are classes
    if isinstance(type_hint, type) and type_hint not in (
        str,
        int,
        float,
        bool,
        bytes,
        list,
        dict,
        tuple,
        set,
        frozenset,
        type(None),
        os.PathLike,
    ):
        referenced.add(type_hint)

    # Handle ForwardRef
    if isinstance(type_hint, ForwardRef):
        # Can't resolve ForwardRefs without context, skip
        return referenced

    # Handle generic types
    origin = get_origin(type_hint)
    args = get_args(type_hint)

    if origin is not None:
        # Add the origin if it's a class (not a built-in generic)
        if isinstance(origin, type) and origin not in (
            list,
            dict,
            tuple,
            set,
            frozenset,
            Union,
            type(None),
            os.PathLike,
        ):
            referenced.add(origin)

        # Recursively extract from args
        for arg in args:
            referenced.update(_extract_referenced_types(arg))

    return referenced


def _get_method_type(cls: type, name: str, member: Any) -> str:  # type: ignore
    """Determine the method type (instance, classmethod, staticmethod)."""
    # Check the class namespace directly to avoid descriptor loss
    if name in cls.__dict__:
        descriptor = cls.__dict__[name]
        if isinstance(descriptor, classmethod):
            return "classmethod"
        if isinstance(descriptor, staticmethod):
            return "staticmethod"
    return "instance"


def _extract_parameters(sig: inspect.Signature) -> list[dict[str, Any]]:  # type: ignore
    """Extract parameter information from a signature."""
    params = []
    for param_name, param in sig.parameters.items():
        param_info = {
            "name": param_name,
            "kind": _get_parameter_kind_name(param.kind),
            "type": _normalize_type_string(param.annotation)
            if param.annotation != inspect.Parameter.empty
            else "__no_annotation__",
            "default": _normalize_default_value(param.default)
            if param.default != inspect.Parameter.empty
            else "__no_default__",
        }
        params.append(param_info)
    return params


def _extract_property_info(prop: property, cls: type) -> dict[str, Any]:  # type: ignore
    """Extract property information."""
    prop_info = {
        "type": "__no_annotation__",
        "has_setter": prop.fset is not None,
        "has_deleter": prop.fdel is not None,
    }

    # Try to get type annotation from the getter
    if prop.fget is not None:
        try:
            sig = inspect.signature(prop.fget)
            if sig.return_annotation != inspect.Signature.empty:
                prop_info["type"] = _normalize_type_string(sig.return_annotation)
        except Exception:
            pass

    return prop_info


def _extract_typeddict_info(cls: type) -> dict[str, Any]:  # type: ignore
    """Extract TypedDict field information."""
    try:
        hints = get_type_hints(cls)
    except Exception:
        hints = {}

    # Determine required vs optional fields
    required_fields = getattr(cls, "__required_keys__", frozenset())
    optional_fields = getattr(cls, "__optional_keys__", frozenset())

    fields = {}
    for field_name, field_type in hints.items():
        if field_name.startswith("_"):
            continue
        fields[field_name] = {
            "required": field_name in required_fields,
            "type": _normalize_type_string(field_type),
        }

    return {"kind": "typeddict", "fields": fields}


def _extract_protocol_info(cls: type) -> dict[str, Any]:  # type: ignore
    """Extract Protocol member information."""
    members = {}

    try:
        for member_name in get_protocol_members(cls):
            if member_name.startswith("_"):
                continue
            member = getattr(cls, member_name, None)
            if member is None:
                continue

            if inspect.isfunction(member):
                try:
                    sig = inspect.signature(member)
                    members[member_name] = {
                        "kind": "method",
                        "parameters": _extract_parameters(sig),
                        "return_type": _normalize_type_string(sig.return_annotation)
                        if sig.return_annotation != inspect.Signature.empty
                        else "__no_annotation__",
                    }
                except Exception:
                    members[member_name] = {
                        "kind": "method",
                        "error": "signature_failed",
                    }
            elif isinstance(member, property):
                members[member_name] = _extract_property_info(member, cls)
    except Exception:
        pass

    return {"kind": "protocol", "members": members}


def _extract_enum_info(cls: type) -> dict[str, Any]:  # type: ignore
    """Extract Enum member information."""
    members = {}
    try:
        for member in cls:  # type: ignore
            members[member.name] = _normalize_default_value(member.value)  # type: ignore
    except Exception:
        # Fallback for enums that can't be iterated
        for name in dir(cls):
            if not name.startswith("_"):
                member = getattr(cls, name)
                if isinstance(member, cls):
                    members[name] = _normalize_default_value(
                        getattr(member, "value", str(member))
                    )

    return {"kind": "enum", "members": members}


def _extract_dataclass_info(cls: type) -> dict[str, Any] | None:  # type: ignore
    """Extract dataclass field information."""
    if not dataclasses.is_dataclass(cls):
        return None

    fields = {}
    for field in dataclasses.fields(cls):
        if field.name.startswith("_"):
            continue
        field_info = {
            "type": _normalize_type_string(field.type)
            if field.type != dataclasses.MISSING
            else "__no_annotation__",
        }
        if field.default != dataclasses.MISSING:
            field_info["default"] = _normalize_default_value(field.default)
        elif field.default_factory != dataclasses.MISSING:
            factory_name = getattr(field.default_factory, "__name__", "<factory>")
            field_info["default_factory"] = f"<factory: {factory_name}>"
        fields[field.name] = field_info

    return {"kind": "dataclass", "fields": fields}


def _extract_class_info(cls: type, result: dict[str, Any]) -> None:  # type: ignore
    """Extract comprehensive information from a class."""
    qualname = f"{cls.__module__}.{cls.__qualname__}"

    if qualname in result["symbols"]:
        return

    # Get base classes
    bases = []
    for base in cls.__bases__:
        if base is not object:
            bases.append(f"{base.__module__}.{base.__name__}")

    class_info: dict[str, Any] = {
        "kind": "class",
        "bases": bases,
        "members": {},
    }

    # Check for special kinds
    if is_typeddict(cls):
        class_info.update(_extract_typeddict_info(cls))
        result["symbols"][qualname] = class_info
        return

    if isinstance(cls, type) and issubclass(cls, enum.Enum):
        class_info.update(_extract_enum_info(cls))
        result["symbols"][qualname] = class_info
        return

    try:
        # Check if it's a Protocol by checking if it's a subclass of Protocol
        # Note: Protocol is a special form, so we need to check the MRO
        if Protocol in getattr(cls, "__bases__", ()):
            class_info.update(_extract_protocol_info(cls))  # type: ignore
            result["symbols"][qualname] = class_info
            return
    except Exception:
        pass

    # Check for dataclass
    dc_info = _extract_dataclass_info(cls)
    if dc_info:
        class_info.update(dc_info)

    # Get type hints for the class
    try:
        type_hints = get_type_hints(cls)
    except Exception:
        type_hints = {}

    # Collect referenced types
    referenced_types = set()

    # Extract annotations-only members
    for name, type_hint in type_hints.items():
        if _should_ignore(name, cls.__module__):
            continue
        if name not in cls.__dict__:
            # Annotation without runtime value
            class_info["members"][name] = {
                "kind": "attribute",
                "type": _normalize_type_string(type_hint),
            }
            referenced_types.update(_extract_referenced_types(type_hint))

    # Extract members from the class namespace
    for name, member in cls.__dict__.items():
        if _should_ignore(name, cls.__module__):
            continue

        if inspect.isfunction(member):
            method_type = _get_method_type(cls, name, member)
            try:
                sig = inspect.signature(member)
                class_info["members"][name] = {
                    "kind": "method",
                    "method_type": method_type,
                    "parameters": _extract_parameters(sig),
                    "return_type": _normalize_type_string(sig.return_annotation)
                    if sig.return_annotation != inspect.Signature.empty
                    else "__no_annotation__",
                }
                # Collect referenced types from signature
                if sig.return_annotation != inspect.Signature.empty:
                    referenced_types.update(
                        _extract_referenced_types(sig.return_annotation)
                    )
                for param in sig.parameters.values():
                    if param.annotation != inspect.Parameter.empty:
                        referenced_types.update(
                            _extract_referenced_types(param.annotation)
                        )
            except Exception:
                class_info["members"][name] = {
                    "kind": "method",
                    "method_type": method_type,
                    "error": "signature_failed",
                }
        elif isinstance(member, property):
            class_info["members"][name] = _extract_property_info(member, cls)
            class_info["members"][name]["kind"] = "property"
            # Collect referenced types from property getter
            if member.fget is not None:
                try:
                    sig = inspect.signature(member.fget)
                    if sig.return_annotation != inspect.Signature.empty:
                        referenced_types.update(
                            _extract_referenced_types(sig.return_annotation)
                        )
                except Exception:
                    pass
        elif isinstance(member, classmethod):
            try:
                sig = inspect.signature(member.__func__)
                class_info["members"][name] = {
                    "kind": "method",
                    "method_type": "classmethod",
                    "parameters": _extract_parameters(sig),
                    "return_type": _normalize_type_string(sig.return_annotation)
                    if sig.return_annotation != inspect.Signature.empty
                    else "__no_annotation__",
                }
                # Collect referenced types from signature
                if sig.return_annotation != inspect.Signature.empty:
                    referenced_types.update(
                        _extract_referenced_types(sig.return_annotation)
                    )
                for param in sig.parameters.values():
                    if param.annotation != inspect.Parameter.empty:
                        referenced_types.update(
                            _extract_referenced_types(param.annotation)
                        )
            except Exception:
                class_info["members"][name] = {
                    "kind": "method",
                    "method_type": "classmethod",
                    "error": "signature_failed",
                }
        elif isinstance(member, staticmethod):
            try:
                sig = inspect.signature(member.__func__)
                class_info["members"][name] = {
                    "kind": "method",
                    "method_type": "staticmethod",
                    "parameters": _extract_parameters(sig),
                    "return_type": _normalize_type_string(sig.return_annotation)
                    if sig.return_annotation != inspect.Signature.empty
                    else "__no_annotation__",
                }
                # Collect referenced types from signature
                if sig.return_annotation != inspect.Signature.empty:
                    referenced_types.update(
                        _extract_referenced_types(sig.return_annotation)
                    )
                for param in sig.parameters.values():
                    if param.annotation != inspect.Parameter.empty:
                        referenced_types.update(
                            _extract_referenced_types(param.annotation)
                        )
            except Exception:
                class_info["members"][name] = {
                    "kind": "method",
                    "method_type": "staticmethod",
                    "error": "signature_failed",
                }
        elif not name.startswith("__") and not inspect.isroutine(member):
            # Class attribute
            attr_type = type_hints.get(name, type(member))
            class_info["members"][name] = {
                "kind": "attribute",
                "type": _normalize_type_string(attr_type),
                "default": _normalize_default_value(member),
            }
            referenced_types.update(_extract_referenced_types(attr_type))

    class_info["referenced_types"] = referenced_types
    result["symbols"][qualname] = class_info


def _extract_function_info(func: Any, module_name: str) -> dict[str, Any]:  # type: ignore
    """Extract information from a module-level function."""
    try:
        sig = inspect.signature(func)
        info = {
            "kind": "function",
            "parameters": _extract_parameters(sig),
            "return_type": _normalize_type_string(sig.return_annotation)
            if sig.return_annotation != inspect.Signature.empty
            else "__no_annotation__",
        }

        # Collect referenced types
        referenced_types = set()
        if sig.return_annotation != inspect.Signature.empty:
            referenced_types.update(_extract_referenced_types(sig.return_annotation))
        for param in sig.parameters.values():
            if param.annotation != inspect.Parameter.empty:
                referenced_types.update(_extract_referenced_types(param.annotation))

        info["referenced_types"] = referenced_types
        return info
    except Exception:
        return {"kind": "function", "error": "signature_failed"}


def _extract_module_info(
    module: Any, result: dict[str, Any], include_all: bool = False
) -> None:  # type: ignore
    """Extract information from a module.

    Args:
        module: The module to extract information from.
        result: The result dictionary to populate.
        include_all: If True, extract all members, not just those in __all__.
    """
    module_name = module.__name__

    # Skip if already processed with include_all=True
    if module_name in result["modules"] and not include_all:
        return

    # Record module exports (only if not already recorded)
    if module_name not in result["modules"]:
        exports = list(getattr(module, "__all__", []))
        result["modules"][module_name] = {
            "kind": "module",
            "exports": sorted(exports),
        }
    else:
        exports = result["modules"][module_name].get("exports", [])

    # Determine which names to process
    if include_all:
        names = dir(module)
    else:
        names = exports

    for name in names:
        if _should_ignore(name, module_name):
            continue

        member = getattr(module, name, None)
        if member is None:
            continue

        # Skip if the member is from a different module (imported)
        if hasattr(member, "__module__") and member.__module__ != module_name:
            if not include_all:
                continue

        if inspect.isclass(member):
            _extract_class_info(member, result)
        elif inspect.isfunction(member):
            qualname = f"{module_name}.{name}"
            # Only add to symbols if not already there
            if qualname not in result["symbols"]:
                result["symbols"][qualname] = _extract_function_info(
                    member, module_name
                )


def _process_referenced_types(result: dict[str, Any]) -> None:  # type: ignore
    """Process all referenced types and add them to the symbols list.

    This function iterates through all extracted symbols, collects their
    referenced types, and adds those types to the symbols list if they're
    not already there.
    """
    # Collect all referenced types from all symbols
    all_referenced = set()
    for symbol_info in result["symbols"].values():
        if "referenced_types" in symbol_info:
            all_referenced.update(symbol_info["referenced_types"])

    # Clean up the internal field from all symbols
    for symbol_info in result["symbols"].values():
        if "referenced_types" in symbol_info:
            del symbol_info["referenced_types"]

    # Add each referenced type to the symbols list
    for ref_type in all_referenced:
        if not inspect.isclass(ref_type):
            continue

        qualname = f"{ref_type.__module__}.{ref_type.__qualname__}"

        # Skip if already in symbols
        if qualname in result["symbols"]:
            continue

        # Skip if in ignored modules
        if _should_ignore(ref_type.__name__, ref_type.__module__):
            continue

        # Extract the class info
        _extract_class_info(ref_type, result)

    # Clean up the internal field from newly added symbols
    for symbol_info in result["symbols"].values():
        if "referenced_types" in symbol_info:
            del symbol_info["referenced_types"]


def _sort_dict(d: dict[str, Any]) -> dict[str, Any]:  # type: ignore
    """Recursively sort dictionaries for deterministic output."""
    if not isinstance(d, dict):
        return d
    return {k: _sort_dict(v) for k, v in sorted(d.items())}


def public_apis() -> dict[str, Any]:  # type: ignore
    """Generate a comprehensive snapshot of the public API.

    Returns:
        A dictionary containing module exports and symbol information.
    """
    result = {"modules": {}, "symbols": {}}

    # Start from drawthings_py.__all__
    _extract_module_info(drawthings_py, result)

    # Also extract from drawthings_py.drawthings to capture grpc() and cli()
    # which are not in __all__ but are part of the public API
    _extract_module_info(drawthings_py.drawthings, result, include_all=True)

    # Start from drawthings_py.configs.__all__
    _extract_module_info(drawthings_py.configs, result)

    # Process referenced types to add them to symbols list
    _process_referenced_types(result)

    # Sort for deterministic output
    result = _sort_dict(result)

    # Save to JSON
    output_path = Path(__file__).parent / "data" / "public_apis.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(result, f, indent=2, sort_keys=True)

    return result


def test_public_apis() -> None:
    """Test that the public API snapshot is up to date."""
    _ = public_apis()
