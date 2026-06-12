from importlib.resources import files
from typing import Required, TypedDict, cast

from strictyaml import (
    Any,
    Map,
    MapPattern,
    Optional,
    Str,
    Float,
    Int,
    Bool,
    Seq,
    load,
)

# Schemas
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
    ignored: Conditional
    optional: object
    versions: list[str]
    unused: bool
    rename: str
    json: list[str] | str
    fbs: Required[FbsDefinition]
    extra_validation: object
    gen_ignore: bool
    group: str


def load_definitions() -> dict[str, PropDefinition]:
    schema = MapPattern(Str(), property_schema)
    yaml_path = files("drawthings_py.resources").joinpath("config_props.yaml")
    yaml_text = yaml_path.read_text()
    yaml = load(yaml_text, schema)
    props_yaml = yaml.data

    definitions = cast(dict[str, PropDefinition], props_yaml)

    for _, value in definitions.items():
        if ignored := value.get("ignored"):
            renamed = cast(
                Conditional, cast(object, {f"_{k}": v for k, v in ignored.items()})
            )
            value["ignored"] = renamed

    return definitions
