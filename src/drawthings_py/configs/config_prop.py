from types import NoneType
from typing import Callable, Generic, TypeVar, cast

from typing_extensions import override

from drawthings_py.generated.dt_grpc.config_generated import (
    ControlT,
    GenerationConfigurationT,
    LoRAT,
)
from drawthings_py._util import ensure_str, snake_to_camel
from .config_dict import ConfigValue, ConfigKey, ConfigDict
from .types import (
    CompressionMethod,
    ControlDict,
    ControlInputType,
    ControlMode,
    LoraDict,
    LoraMode,
    SeedModeHelpers,
    SamplerHelpers,
    SamplerType,
    SeedMode,
    UpscalerModel,
    control_dict_from_json,
)

from .prop_schema import Conditional, PropDefinition, load_definitions


T = TypeVar("T", covariant=True, bound=ConfigValue)


class ConfigProp(Generic[T]):
    name: ConfigKey
    fbs_name: str
    json_name: str
    all_names: list[str]
    config_t_name: str
    value_type: type = NoneType

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
        val = cast(T | None, getattr(config_t, self.config_t_name))
        if val is None:
            return None
        if isinstance(val, bytes):
            val = val.decode("utf-8")
        return self._from_fbs_value(val)

    def _from_fbs_value(self, value: object) -> T | None:
        try:
            if isinstance(value, self.value_type):
                return cast(T, value)
        except Exception:
            print("Exceptional", self.name)
            return None
        return None

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

        if (value := self._to_fbs_value(config)) is not None:
            setattr(out, self.config_t_name, value)

    def _to_fbs_value(self, config: ConfigDict) -> object | None:
        return config.get(self.name)

    def _get_ignore(self, con: Conditional) -> Callable[[ConfigDict], bool]:
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
    def default(self) -> T:
        raise NotImplementedError


class IntProp(ConfigProp[int]):
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
        if isinstance(value, str | int | float):
            return int(value)
        return None

    @override
    def _from_fbs_value(self, value: object) -> int | None:
        if isinstance(value, int | float):
            return int(value * self.unit)
        return None

    @override
    def _to_fbs_value(self, config: ConfigDict) -> int:
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
        self.value_type: type = float
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
        self.value_type: type = bool
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
        self.value_type: type = str
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


class SamplerProp(ConfigProp[str]):
    def __init__(self, name: ConfigKey, definition: PropDefinition):
        super().__init__(name, definition)
        self.value_type: type = str

    @override
    def _from_json_value(self, value: object) -> SamplerType | None:
        return SamplerHelpers.from_value(value)

    @override
    def _from_fbs_value(self, value: object) -> SamplerType | None:
        return SamplerHelpers.from_value(value)

    @override
    def _to_fbs_value(self, config: ConfigDict) -> int | None:
        if val := cast(object, config.get(self.name)):
            return SamplerHelpers.to_int(val)
        return None

    @property
    @override
    def default(self) -> SamplerType:
        return "DPMPP2MKarras"


class LorasProp(ConfigProp[list[LoraDict]]):
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
    def _from_fbs_value(self, value: object) -> list[LoraDict] | None:
        if isinstance(value, list):
            loras = [self._lorat_to_loradict(lora) for lora in cast(list[LoRAT], value)]
            return [lora for lora in loras if lora is not None]
        return super()._from_fbs_value(value)

    @override
    def _to_fbs_value(self, config: ConfigDict) -> list[LoRAT]:
        if loras := config.get("loras"):
            lorats = [self._loradict_to_lorat(lora) for lora in loras]
            return [lora for lora in lorats if lora is not None]
        return []

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
                "mode": LoraMode.from_value(mode),
            }
        )

    @classmethod
    def _loradict_to_lorat(cls, lora: LoraDict) -> LoRAT | None:
        file = lora.get("file")
        if not file:
            return None
        weight = lora.get("weight", 1.0)
        mode = LoraMode.from_value(lora.get("mode", LoraMode.All))

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
        mode = LoraMode.from_value(json.get("mode", LoraMode.All))

        return LoraDict({"file": file, "weight": weight, "mode": mode})


class ControlsProp(ConfigProp[list[ControlDict]]):
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
        return super()._from_fbs_value(value)

    @override
    def _to_fbs_value(self, config: ConfigDict) -> list[ControlT]:
        if controls := config.get("controls"):
            controlts = [self._controldict_to_controlt(control) for control in controls]
            return [control for control in controlts if control is not None]
        return []

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
                "controlMode": ControlMode.from_value(cast(int, controlt.controlMode)),
                "targetBlocks": controlt.targetBlocks if controlt.targetBlocks else [],
                "inputOverride": ControlInputType.from_value(
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
            controlMode=ControlMode.from_value(
                control.get("controlMode", ControlMode.Balanced)
            ),
            targetBlocks=control.get("targetBlocks", []),
            inputOverride=ControlInputType.from_value(
                control.get("inputOverride", ControlInputType.Unspecified)
            ),
        )


class SeedModeProp(ConfigProp[SeedMode]):
    def __init__(self, name: ConfigKey, definition: PropDefinition):
        super().__init__(name, definition)
        self.value_type: type = str

    @override
    def _from_json_value(self, value: object) -> SeedMode | None:
        return SeedModeHelpers.from_value(value)

    @override
    def _from_fbs_value(self, value: object) -> SeedMode | None:
        return SeedModeHelpers.from_value(value)

    @override
    def _to_fbs_value(self, config: ConfigDict) -> int | None:
        if val := cast(object, config.get(self.name)):
            return SeedModeHelpers.to_int(val)
        return None

    @property
    @override
    def default(self) -> SeedMode:
        return "ScaleAlike"


class CompressionArtifactsProps(ConfigProp[CompressionMethod]):
    def __init__(self, name: ConfigKey, definition: PropDefinition):
        super().__init__(name, definition)
        self.value_type: type = CompressionMethod

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

    @property
    @override
    def default(self) -> UpscalerModel | None:
        return None


def load_props() -> dict[ConfigKey, ConfigProp[ConfigValue]]:
    props: dict[ConfigKey, ConfigProp[ConfigValue]] = {}

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
