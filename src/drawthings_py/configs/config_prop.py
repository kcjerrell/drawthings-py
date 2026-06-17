from abc import ABC, abstractmethod
import json
from types import NoneType
from typing import Callable, Generic, Protocol, TypeVar, cast

from typing_extensions import override

from drawthings_py.configs.enums import (
    ENUM_HELPER_MAP,
    EnumTypes,
    control_input_type_from_value,
    control_input_type_to_int,
    control_mode_from_value,
    control_mode_to_int,
    lora_mode_from_value,
    lora_mode_to_int,
)
from drawthings_py.generated.dt_grpc.config_generated import (
    ControlT,
    GenerationConfigurationT,
    LoRAT,
)
from drawthings_py.util._util import (
    ensure_str,
    random_seed,
    snake_to_camel,
    try_parse_float,
    try_parse_int,
)
from .config_dict import ConfigDict, ConfigKey, ConfigValue
from .types import (
    ControlDict,
    LoraDict,
    UpscalerModel,
    control_dict_from_json,
)

from .prop_schema import Conditional, PropDefinition, load_definitions


T = TypeVar("T", bound=ConfigValue)
U = TypeVar("U", bound=int | float | str | bool | None | list[LoRAT] | list[ControlT])


class ConfigProp(Protocol):
    name: ConfigKey

    def from_fbs(self, config_t: GenerationConfigurationT) -> ConfigValue | None: ...
    def from_json(self, data: dict[str, object]) -> ConfigValue | None: ...
    def to_fbs(
        self,
        config: ConfigDict,
        out: GenerationConfigurationT,
        override: object | None,
    ) -> None: ...

    @property
    def default(self) -> ConfigValue: ...


class ConfigPropBase(ConfigProp, Generic[T, U], ABC):
    """
    Base class for representing a config property at run time. Handles conversion to/from
    JSON and flatbuffer. Interprets the provided YAML property definition to handle
    type conversions and some validation.
    """

    name: ConfigKey
    """The name of the property in the python API"""
    fbs_name: str
    """the name of the property in the flatbuffer schema"""
    json_name: str
    """the property's canonical JSON name, as exported by DT"""
    all_names: list[str]
    """a list of all names that this property might have"""
    config_t_name: str
    """this property's name on the GenerationConfigurationT builder"""
    value_type: type = NoneType
    """the type of this property"""

    _ignored: Callable[[ConfigDict], bool] | None = None
    """
    a callable that, when provided with a config, determines if this property should
    be ignored
    """

    def __init__(self, name: ConfigKey, definition: PropDefinition):
        self.name = name
        self.fbs_name = definition["fbs"].get("name", name)
        json_def = definition.get("json", None)
        json_names = (
            json_def if isinstance(json_def, list) else [json_def] if json_def else []
        )
        self.json_name = json_names[0] if json_names else self.name
        self.all_names = list(set([self.name, self.fbs_name] + json_names))
        self.config_t_name = snake_to_camel(self.fbs_name)

        if ignored := definition.get("ignored"):
            self._ignored = self._get_ignore(ignored)

    @override
    def from_json(self, data: dict[str, object]) -> T | None:
        """finds and returns this property's value in the provided JSON dict"""
        for name in self.all_names:
            if name in data:
                return self._from_json_value(data[name])
        return None

    @abstractmethod
    def _from_json_value(self, value: object) -> T | None:
        """
        when provided with a value (as loaded from JSON), returns the property's
        python equivalent. Must be overriden by subclasses.
        """
        return None

    @override
    def from_fbs(self, config_t: GenerationConfigurationT) -> T | None:
        """when provided with the flatbuffer object, returns this property's value"""
        if not hasattr(config_t, self.config_t_name):
            return None
        val = cast(object, getattr(config_t, self.config_t_name))
        if val is None:
            return None
        if isinstance(val, bytes):
            val = val.decode("utf-8")
        return self._from_fbs_value(cast(U, val))

    def _from_fbs_value(self, value: U | None) -> T | None:
        """
        when provided with a value (as loaded from flatbuffer), returns the property's
        python equivalent
        """
        try:
            if isinstance(value, self.value_type):
                return cast(T, value)
        except Exception:
            print("Exceptional", self.name)
            return None
        return None

    @override
    def to_fbs(
        self,
        config: ConfigDict,
        out: GenerationConfigurationT,
        override: object | None = None,
    ) -> None:
        """ "
        when provided with a config and a flatbuffer object, sets this property's
        value on the flatbuffer
        """
        if self._ignored and self._ignored(config):
            return

        config_value = cast(
            T, override if override is not None else config.get(self.name)
        )

        if (value := self._to_fbs_value(config_value)) is not None:
            setattr(out, self.config_t_name, value)

    @abstractmethod
    def _to_fbs_value(self, value: T) -> U:
        pass

    def _get_ignore(self, con: Conditional) -> Callable[[ConfigDict], bool]:
        """transforms the 'ignored' conditional block from yaml into a callable"""
        if_val = con.get("_if")
        if_not_val = con.get("_not_if")
        op1_key = cast(ConfigKey, if_val or if_not_val)

        if eq_val := con.get("_eq"):
            return lambda config: cast(bool, config.get(op1_key) == eq_val)
        if neq_val := con.get("_neq"):
            return lambda config: cast(bool, config.get(op1_key) != neq_val)
        if in_val := con.get("_in"):
            return lambda config: config.get(op1_key) in in_val
        return lambda config: bool(config.get(op1_key))

    @property
    @override
    @abstractmethod
    def default(self) -> T:
        pass


class IntProp(ConfigPropBase[int, int]):
    unit: int = 1
    _default: int = 0

    def __init__(self, name: ConfigKey, definition: PropDefinition):
        super().__init__(name, definition)
        self.value_type: type = int
        if fbs := definition.get("fbs"):
            if unit := fbs.get("unit"):
                self.unit = int(unit)

        if default := definition.get("default"):
            self._default = int(default)

    @override
    def _from_json_value(self, value: object) -> int | None:
        return try_parse_int(value)

    @override
    def _from_fbs_value(self, value: object) -> int | None:
        if (int_value := try_parse_int(value)) is not None:
            return int(int_value * self.unit)
        return None

    @override
    def _to_fbs_value(self, value: int | None) -> int:
        if value is None:
            return self.default if self.name != "seed" else random_seed()
        # this is a workaround for now
        if self.name == "seed" and value == -1:
            return random_seed()
        return int(round(value / self.unit))

    @property
    @override
    def default(self) -> int:
        return self._default


class FloatProp(ConfigPropBase[float, float]):
    _default: float = 0.0

    def __init__(self, name: ConfigKey, definition: PropDefinition):
        super().__init__(name, definition)
        self.value_type: type = float
        if default := definition.get("default"):
            self._default = float(default)

    @override
    def _from_json_value(self, value: object) -> float | None:
        return try_parse_float(value)

    @override
    def _from_fbs_value(self, value: object) -> float | None:
        return try_parse_float(value)

    @override
    def _to_fbs_value(self, value: float | None) -> float:
        if value is None:
            return self.default
        return float(value)

    @property
    @override
    def default(self) -> float:
        return self._default


class BoolProp(ConfigPropBase[bool, bool]):
    _default: bool = False

    def __init__(self, name: ConfigKey, definition: PropDefinition):
        super().__init__(name, definition)
        self.value_type: type = bool
        if default := definition.get("default"):
            self._default = default.lower() not in ("false", "0", "")

    @override
    def _from_json_value(self, value: object) -> bool | None:
        if isinstance(value, bool):
            return value
        return None

    @override
    def _from_fbs_value(self, value: bool | None) -> bool | None:
        return value

    @override
    def _to_fbs_value(self, value: bool | None) -> bool:
        return value if value is not None else self.default

    @property
    @override
    def default(self) -> bool:
        return self._default


class StringProp(ConfigPropBase[str | None, str | None]):
    _default: str | None = None

    def __init__(self, name: ConfigKey, definition: PropDefinition):
        super().__init__(name, definition)
        self.value_type: type = str
        if default := definition.get("default"):
            self._default = default

    @override
    def _from_json_value(self, value: object) -> str | None:
        if isinstance(value, str):
            return value
        return None

    @override
    def _from_fbs_value(self, value: str | None) -> str | None:
        return ensure_str(value)

    @override
    def _to_fbs_value(self, value: str | None) -> str | None:
        return value if value is not None else self.default

    @property
    @override
    def default(self) -> str | None:
        return self._default


class LorasProp(ConfigPropBase[list[LoraDict], list[LoRAT]]):
    def __init__(self, name: ConfigKey, definition: PropDefinition):
        super().__init__(name, definition)
        self.value_type: type = list[LoraDict]

    @override
    def _from_json_value(self, value: object) -> list[LoraDict]:
        if isinstance(value, list):
            loras = [self._json_to_loradict(lora) for lora in cast(list[object], value)]
            return [lora for lora in loras if lora is not None]
        return []

    @override
    def _from_fbs_value(self, value: list[LoRAT] | None) -> list[LoraDict] | None:
        if isinstance(value, list):
            loras = [self._lorat_to_loradict(lora) for lora in value]
            return [lora for lora in loras if lora is not None]
        return self.default

    @override
    def _to_fbs_value(self, value: list[LoraDict] | None) -> list[LoRAT]:
        if value is None:
            return []
        lorats = [self._loradict_to_lorat(lora) for lora in value]
        return [lora for lora in lorats if lora is not None]

    @property
    @override
    def default(self) -> list[LoraDict]:
        return []

    @classmethod
    def _lorat_to_loradict(cls, lorat: LoRAT) -> LoraDict | None:
        file, weight, mode = ensure_str(lorat.file), lorat.weight, cast(int, lorat.mode)
        print(file, weight, mode)
        if not isinstance(file, str) or not isinstance(weight, float):
            return None

        return LoraDict(
            {
                "file": file,
                "weight": weight,
                "mode": lora_mode_from_value(mode),
            }
        )

    @classmethod
    def _loradict_to_lorat(cls, lora: LoraDict) -> LoRAT | None:
        file = lora.get("file")
        if not file:
            return None
        weight = lora.get("weight", 1.0)
        mode = lora_mode_to_int(lora.get("mode"))

        return LoRAT(file, weight, mode)

    @classmethod
    def _json_to_loradict(cls, json: object) -> LoraDict | None:
        if not isinstance(json, dict):
            return None
        json = cast(dict[str, object], json)
        file = ensure_str(json.get("file"))
        if not file:
            return None
        weight = float(cast(str | float | int | None, json.get("weight")) or 1.0)
        mode = lora_mode_from_value(json.get("mode"))

        return LoraDict({"file": file, "weight": weight, "mode": mode})


class ControlsProp(ConfigPropBase[list[ControlDict], list[ControlT]]):
    def __init__(self, name: ConfigKey, definition: PropDefinition):
        super().__init__(name, definition)
        self.value_type: type = list[ControlDict]

    @override
    def _from_json_value(self, value: object) -> list[ControlDict]:
        if isinstance(value, list):
            controls = [
                control_dict_from_json(control) for control in cast(list[object], value)
            ]
            return [control for control in controls if control is not None]
        return []

    @override
    def _from_fbs_value(self, value: object) -> list[ControlDict] | None:
        if isinstance(value, list):
            controls = [
                self._controlt_to_controldict(control)
                for control in cast(list[ControlT], value)
            ]
            return [control for control in controls if control is not None]
        return self.default

    @override
    def _to_fbs_value(self, value: list[ControlDict] | None) -> list[ControlT]:
        if value is None:
            return []
        controlts = [self._controldict_to_controlt(control) for control in value]
        return [control for control in controlts if control is not None]

    @property
    @override
    def default(self) -> list[ControlDict]:
        return []

    @classmethod
    def _controlt_to_controldict(cls, controlt: ControlT) -> ControlDict | None:
        file = ensure_str(controlt.file)
        if not isinstance(file, str):
            return None

        return ControlDict(
            {
                "file": file,
                "weight": controlt.weight,
                "guidanceStart": controlt.guidanceStart,
                "guidanceEnd": controlt.guidanceEnd,
                "noPrompt": controlt.noPrompt,
                "globalAveragePooling": controlt.globalAveragePooling,
                "downSamplingRate": controlt.downSamplingRate,
                "controlMode": control_mode_from_value(cast(int, controlt.controlMode)),
                "targetBlocks": controlt.targetBlocks if controlt.targetBlocks else [],
                "inputOverride": control_input_type_from_value(
                    cast(int, controlt.inputOverride)
                ),
            }
        )

    @classmethod
    def _controldict_to_controlt(cls, control: ControlDict) -> ControlT | None:
        file = control.get("file")
        if not file:
            return None

        return ControlT(
            file=file,
            weight=control.get("weight", 1.0),
            guidanceStart=control.get("guidanceStart", 0.0),
            guidanceEnd=control.get("guidanceEnd", 1.0),
            noPrompt=control.get("noPrompt", False),
            globalAveragePooling=control.get("globalAveragePooling", True),
            downSamplingRate=control.get("downSamplingRate", 1.0),
            controlMode=control_mode_to_int(control.get("controlMode")),
            targetBlocks=control.get("targetBlocks", []),
            inputOverride=control_input_type_to_int(control.get("inputOverride")),
        )


class UpscalerModelProp(ConfigPropBase[UpscalerModel | None, str | None]):
    def __init__(self, name: ConfigKey, definition: PropDefinition):
        super().__init__(name, definition)
        self.value_type: type = UpscalerModel

    @override
    def _from_json_value(self, value: object) -> UpscalerModel | None:
        if isinstance(value, str):
            return UpscalerModel.from_value(value)
        return None

    @override
    def _from_fbs_value(self, value: object) -> UpscalerModel | None:
        if name := ensure_str(value):
            return UpscalerModel.from_value(name)
        return None

    @override
    def _to_fbs_value(self, value: UpscalerModel | None) -> str | None:
        return value.value if value is not None else None

    @property
    @override
    def default(self) -> UpscalerModel | None:
        return None


V = TypeVar("V", covariant=True, bound=EnumTypes)


class StrEnumProp(ConfigPropBase[str, int], Generic[V]):
    _to_int: Callable[[str | None], int]
    _from_value: Callable[[object], str]
    _default: V

    def __init__(self, name: ConfigKey, definition: PropDefinition):
        super().__init__(name, definition)
        self.value_type: type = str

        enum_type = cast(str, definition.get("type"))
        if enum_type not in ENUM_HELPER_MAP:
            raise ValueError(f"Unknown enum type: {enum_type}")

        (self._from_value, self._to_int) = ENUM_HELPER_MAP[enum_type]

        self._default = cast(V, self._from_value(-1))

    @override
    def _from_json_value(self, value: object) -> V | None:
        return cast(V, self._from_value(value))

    @override
    def _from_fbs_value(self, value: object) -> str | None:
        return cast(V, self._from_value(value))

    @override
    def _to_fbs_value(self, value: str | None) -> int:
        return self._to_int(value)

    @property
    @override
    def default(self) -> str:
        return self._default


_config_props: dict[ConfigKey, ConfigProp] | None = None


def load_props() -> dict[ConfigKey, ConfigProp]:
    global _config_props
    if _config_props:
        return _config_props

    props: dict[ConfigKey, ConfigProp] = {}

    definitions = cast(dict[ConfigKey, PropDefinition], load_definitions())

    for key, value in definitions.items():
        prop_type = value.get("type")
        if prop_type == "int":
            props[key] = IntProp(key, value)
        elif prop_type == "float":
            props[key] = FloatProp(key, value)
        elif prop_type == "bool":
            props[key] = BoolProp(key, value)
        elif prop_type == "str" or prop_type == "str | None":
            props[key] = StringProp(key, value)
        elif key in ["sampler", "seed_mode", "compression_artifacts"]:
            props[key] = StrEnumProp(key, value)
        elif prop_type == "list[LoraDict]":
            props[key] = LorasProp(key, value)
        elif prop_type == "list[ControlDict]":
            props[key] = ControlsProp(key, value)
        elif prop_type == "UpscalerModel | None":
            props[key] = UpscalerModelProp(key, value)
        else:
            print(f"Unknown config property type in YAML: {key}: {prop_type}")

    _config_props = props
    return props


def config_dict_from_json(json_data: str | dict[str, object]) -> ConfigDict:
    if isinstance(json_data, str):
        data = cast(dict[str, object], json.loads(json_data))
    else:
        data = json_data
    config = ConfigDict()
    for prop in load_props().values():
        if value := prop.from_json(data):
            config[prop.name] = value  # pyright: ignore[reportGeneralTypeIssues]
    return config


def config_dict_from_fbs(data: bytes) -> ConfigDict:
    config_t = GenerationConfigurationT.InitFromPackedBuf(data)
    config = ConfigDict()
    for prop in load_props().values():
        value = prop.from_fbs(config_t)
        if value is not None:
            config[prop.name] = value  # pyright: ignore[reportGeneralTypeIssues]
    return config
