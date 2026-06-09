from typing import Callable, Generic, Required, TypeVar, TypedDict, cast

from strictyaml import Any, Map, MapPattern, Optional, Str, Float, Int, Bool, Seq, load
from typing_extensions import override

from drawthings_py._util import snake_to_camel
from drawthings_py.configs.config_dict import ConfigValue, ConfigKey, ConfigDict
from drawthings_py.configs.types import (
    CompressionMethod,
    ControlDict,
    LoraDict,
    SamplerType,
    SeedMode,
    UpscalerModel,
)
from drawthings_py.generated.dt_grpc.config_generated import GenerationConfigurationT

conditional_schema = Map(
    {
        Optional("if"): Str(),
        Optional("if_not"): Str(),
        Optional("then"): Str(),
        Optional("else"): Str(),
        Optional("eq"): Str(),
        Optional("neq"): Str(),
        Optional("in"): Seq(Str()),
    }
)

fbs_schema = Map(
    {
        Optional("name"): Str(),
        "type": Str(),
        Optional("unit"): Int(),
        Optional("min"): Int() | Float(),
        Optional("max"): Int() | Float(),
        Optional("convert"): Str(),
    }
)

property_schema = Map(
    {
        "type": Str(),
        Optional("default"): Str(),
        Optional("min"): Float() | Int(),
        Optional("max"): Float() | Int() | Any(),
        Optional("description"): Str(),
        Optional("ignored"): conditional_schema,
        Optional("optional"): Any(),
        Optional("versions"): Seq(Str()),
        Optional("unused"): Bool(),
        Optional("rename"): Str(),
        Optional("json"): Seq(Str()) | Str(),
        Optional("fbs"): fbs_schema,
        Optional("extra_validation"): Any(),
        Optional("gen_ignore"): Bool(),
        Optional("group"): Str(),
    }
)


class Conditional(TypedDict, total=False):
    _if: str
    _if_not: str
    _then: str
    _else: str
    _eq: str
    _neq: str
    _in: list[str]


class FbsDefinition(TypedDict, total=False):
    name: str
    type: str
    unit: int


class PropDefinition(TypedDict, total=False):
    type: str
    default: str
    min: float | int
    max: float | int | object
    description: str
    ignored: bool | Conditional
    optional: object
    versions: list[str]
    unused: bool
    rename: str
    json: list[str] | str
    fbs: Required[FbsDefinition]
    extra_validation: object
    gen_ignore: bool
    group: str


T = TypeVar("T", covariant=True, bound=ConfigValue)


class ConfigProp(Generic[T]):
    name: ConfigKey
    fbs_name: str
    json_name: str
    all_names: list[str]
    config_t_name: str

    _ignored: Callable[[ConfigDict], bool] | None = None

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
            if isinstance(ignored, dict):
                self._ignored = self._get_ignore(ignored)

    def from_json(self, data: dict[str, object]) -> T | None:
        for name in self.all_names:
            if name in data:
                return self._from_json_value(data[name])
        return None

    def _from_json_value(self, value: object) -> T | None:  # pyright: ignore[reportUnusedParameter]
        return None

    def from_fbs(self, config_t: GenerationConfigurationT) -> T | None:
        if not hasattr(config_t, self.config_t_name):
            return None
        val = getattr(config_t, self.config_t_name)
        if val is None:
            return None
        if isinstance(val, bytes):
            val = val.decode("utf-8")
        return self._from_fbs_value(val)

    def _from_fbs_value(self, value: object) -> T | None:
        return self._from_json_value(value)


    def to_fbs(
        self,
        config: ConfigDict,
        out: GenerationConfigurationT,
        override: ConfigValue | None = None,
    ) -> None:
        if self._ignored and self._ignored(config):
            return

        if override is not None:
            setattr(out, self.config_t_name, override)
            return

        if (value := self._get_fbs_value(config)) is not None:
            setattr(out, self.config_t_name, value)

    def _get_fbs_value(self, config: ConfigDict) -> object | None:
        return config.get(self.name)

    def _get_ignore(self, con: Conditional) -> Callable[[ConfigDict], bool]:
        if_val = con.get("_if")
        if_not_val = con.get("_not_if")
        op1_key = cast(ConfigKey, if_val or if_not_val)

        if eq_val := con.get("_eq"):
            return lambda config: config.get(op1_key) == eq_val
        if neq_val := con.get("_neq"):
            return lambda config: config.get(op1_key) != neq_val
        if in_val := con.get("_in"):
            return lambda config: config.get(op1_key) in in_val
        return lambda config: bool(config.get(op1_key))

    @property
    def default(self) -> T:
        raise NotImplementedError


class IntProp(ConfigProp[int]):
    unit: int = 1
    _default: int = 0

    def __init__(self, name: ConfigKey, definition: PropDefinition):
        super().__init__(name, definition)
        if fbs := definition.get("fbs"):
            if unit := fbs.get("unit"):
                self.unit = int(unit)

        if default := definition.get("default"):
            self._default = int(default)

    @override
    def _from_json_value(self, value: object) -> int | None:
        if isinstance(value, str | int | float):
            return int(value)
        return None

    @override
    def _from_fbs_value(self, value: object) -> int | None:
        if isinstance(value, int | float):
            return int(value * self.unit)
        return None

    @override
    def _get_fbs_value(self, config: ConfigDict) -> int:
        value = cast(int | None, config.get(self.name))
        if value is None:
            return 0
        return int(round(value / self.unit))

    @property
    @override
    def default(self) -> int:
        return self._default


class FloatProp(ConfigProp[float]):
    _default: float = 0.0

    def __init__(self, name: ConfigKey, definition: PropDefinition):
        super().__init__(name, definition)
        if default := definition.get("default"):
            self._default = float(default)

    @override
    def _from_json_value(self, value: object) -> float | None:
        if isinstance(value, str | int | float):
            return float(value)
        return None

    @property
    @override
    def default(self) -> float:
        return self._default


class BoolProp(ConfigProp[bool]):
    _default: bool = False

    def __init__(self, name: ConfigKey, definition: PropDefinition):
        super().__init__(name, definition)
        if default := definition.get("default"):
            self._default = default.lower() not in ("false", "0", "")

    @override
    def _from_json_value(self, value: object) -> bool | None:
        if isinstance(value, bool):
            return value
        return None

    @property
    @override
    def default(self) -> bool:
        return self._default


class StringProp(ConfigProp[str | None]):
    _default: str | None = None

    def __init__(self, name: ConfigKey, definition: PropDefinition):
        super().__init__(name, definition)
        if default := definition.get("default"):
            self._default = default

    @override
    def _from_json_value(self, value: object) -> str | None:
        if isinstance(value, str):
            return value
        return None

    @property
    @override
    def default(self) -> str | None:
        return self._default


class SamplerProp(ConfigProp[SamplerType]):
    @override
    def _from_json_value(self, value: object) -> SamplerType | None:
        if isinstance(value, str | int):
            return SamplerType.from_value(value)
        return None

    @property
    @override
    def default(self) -> SamplerType:
        return SamplerType.DDIM


class LorasProp(ConfigProp[list[LoraDict]]):
    @override
    def _from_json_value(self, value: object) -> list[LoraDict]:
        if isinstance(value, list):
            return [LoraDict(**lora) for lora in value]
        return []

    @property
    @override
    def default(self) -> list[LoraDict]:
        return []


class ControlsProp(ConfigProp[list[ControlDict]]):
    @override
    def _from_json_value(self, value: object) -> list[ControlDict]:
        if isinstance(value, list):
            return [ControlDict(**control) for control in value]
        return []

    @property
    @override
    def default(self) -> list[ControlDict]:
        return []


class SeedModeProp(ConfigProp[SeedMode]):
    @override
    def _from_json_value(self, value: object) -> SeedMode | None:
        if isinstance(value, str | int):
            return SeedMode.from_value(value)
        return None

    @property
    @override
    def default(self) -> SeedMode:
        return SeedMode.ScaleAlike


class CompressionArtifactsProps(ConfigProp[CompressionMethod]):
    @override
    def _from_json_value(self, value: object) -> CompressionMethod | None:
        if isinstance(value, str | int):
            return CompressionMethod.from_value(value)
        return None

    @property
    @override
    def default(self) -> CompressionMethod:
        return CompressionMethod.Disabled


class UpscalerModelProp(ConfigProp[UpscalerModel | None]):
    @override
    def _from_json_value(self, value: object) -> UpscalerModel | None:
        if isinstance(value, str):
            return UpscalerModel.from_value(value)
        return None

    @property
    @override
    def default(self) -> UpscalerModel | None:
        return None


def load_props() -> dict[ConfigKey, ConfigProp[ConfigValue]]:
    schema = MapPattern(Str(), property_schema)
    json_text = open("./resources/config_props.yaml", "r").read()
    yaml = load(json_text, schema)
    props_yaml = yaml.data
    props: dict[ConfigKey, ConfigProp[ConfigValue]] = {}

    definitions = cast(dict[ConfigKey, PropDefinition], props_yaml)

    for key, value in definitions.items():
        if ignore := value.get("ignored"):
            renamed = {f"_{k}": v for k, v in ignore.items()}
            value["ignored"] = Conditional(**renamed)

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
        elif prop_type == "SamplerType":
            props[key] = SamplerProp(key, value)
        elif prop_type == "SeedMode":
            props[key] = SeedModeProp(key, value)
        elif prop_type == "CompressionMethod":
            props[key] = CompressionArtifactsProps(key, value)
        elif prop_type == "list[LoraDict]":
            props[key] = LorasProp(key, value)
        elif prop_type == "list[ControlDict]":
            props[key] = ControlsProp(key, value)
        elif prop_type == "UpscalerModel | None":
            props[key] = UpscalerModelProp(key, value)
        else:
            print(f"Unknown config property type in YAML: {key}: {prop_type}")
            props[key] = ConfigProp(key, value)

    return props


# load_props()
