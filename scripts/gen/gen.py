from textwrap import dedent, indent

from config_props import ConfigProp
from strictyaml import (
    Bool,
    Any,
    Enum,
    Float,
    Int,
    Map,
    MapPattern,
    Optional,
    Str,
    as_document,
    load,
    Seq,
    compound,
)


def tab(text: str, level: int = 1) -> str:
    return indent(text, "    " * level)


class ConfigCodeGen:
    props: list[ConfigProp[Any]]
    imports: set[tuple[str, str | None]]

    accessors: str | None
    config_dict: str | None
    from_json: str | None
    to_fbs: str | None
    from_fbs: str | None
    validate: str | None
    class_def: str | None

    def __init__(self):
        self.props = []
        self.imports = set()
        self.accessors = None
        self.config_dict = None
        self.from_json = None
        self.to_fbs = None
        self.from_fbs = None
        self.validate = None
        self.class_def = """
class GenConfig:
    _data: ConfigDict

    def __init__(self, **kwargs: Unpack[ConfigDict]):
        self._data = ConfigDict(**kwargs)
                """
        self.imports.add(("typing", "Unpack"))
        self.from_dict = tab(
            """
@classmethod
def from_dict(cls, data: ConfigDict):
    return cls(**data)

def update(self, data: ConfigDict):
    self._data.update(data)
        """,
            1,
        )

    def load_props(self, yaml_path: str):
        property_schema = Map(
            {
                "type": Str(),
                Optional("default"): Any(),
                Optional("min"): Float() | Int(),
                Optional("max"): Float() | Int() | Any(),
                Optional("description"): Str(),
                Optional("ignored"): Bool() | Any(),
                Optional("optional"): Any(),
                Optional("versions"): Seq(Str()),
                Optional("unused"): Bool(),
                Optional("rename"): Str(),
                Optional("json"): Seq(Str()) | Str(),
                Optional("fbs"): Any(),
                Optional("extra_validation"): Any(),
            }
        )
        schema = MapPattern(Str(), property_schema)
        json_text = open("./resources/config_props.yaml", "r").read()
        yaml = load(json_text, schema)
        print(yaml.is_mapping())
        props_yaml = yaml.data
        self.props = [ConfigProp(key, value) for key, value in props_yaml.items()]

    def gen_dict(self):
        self.imports.add(("typing", "TypedDict"))
        fields: list[str] = []
        for prop in self.props:
            prop_type: str = prop.schema.get("type")
            fields.append(f"{prop.name}: {prop_type}")
            if prop_type.replace(" | None", "") not in ["str", "int", "float", "bool"]:
                self.imports.add((".types", prop_type.replace(" | None", "")))

        fields_code = tab("\n".join(fields), 1)
        self.config_dict = """class ConfigDict(TypedDict, total=False):\n"""
        self.config_dict += fields_code

    def gen_imports(self):
        self.imports.add(("typing", "cast"))

        imports_modules: dict[str, list[str] | None] = {}
        for im_module, im_name in self.imports:
            if im_module not in imports_modules:
                imports_modules[im_module] = [] if im_name is not None else None
            if im_name is not None:
                imports_modules[im_module].append(im_name)  # type: ignore

        imports_code: list[str] = []

        for im_module, im_names in imports_modules.items():
            if im_names is None:
                imports_code.append(f"import {im_module}")
            else:
                if im_module == "__future__":
                    imports_code.insert(
                        0, f"from {im_module} import {', '.join(im_names)}"
                    )
                else:
                    imports_code.append(
                        f"from {im_module} import {', '.join(im_names)}"
                    )

        return "\n".join(imports_code)

    def gen_accessors(self):
        props_codes: list[str] = []
        for prop in self.props:
            prop.gen_prop_alt(props_codes, [], self.imports)
        self.accessors = tab("\n".join(props_codes), 1)

    def gen_from_json(self):
        self.imports.add(("json", None))
        self.imports.add(("__future__", "annotations"))
        self.imports.add(("typing", "Any"))
        props_codes: list[str] = []
        for prop in self.props:
            prop.gen_from_json(props_codes, self.imports)
        prop_code = tab("\n".join(props_codes), 1)
        from_json_def = """@classmethod
def from_json(cls, json_text: str | None = None, json_data: ConfigDict | None = None) -> GenConfig:
    data = json_data if json_data is not None else cast(dict[str, Any], json.loads(json_text or "{}"))  # pyright: ignore[reportExplicitAny]
    config_dict = ConfigDict()\n"""
        from_json_return = tab("\nreturn GenConfig.from_dict(config_dict)", 1)
        self.from_json = tab(from_json_def + prop_code + from_json_return)

    def gen_to_fbs(self):
        self.imports.add(("flatbuffers", None))
        self.imports.add(
            (
                "drawthings_py.generated.dt_grpc.config_generated",
                "GenerationConfigurationT",
            )
        )
        props_by_name = {prop.name: prop for prop in self.props}
        props_codes: list[str] = []
        for prop in self.props:
            prop.gen_to_fbs(
                props_codes, props_by_name, "seed" if prop.name == "seed" else None
            )
        prop_code = tab("\n".join(props_codes), 1)
        to_fbs_def = dedent("""
def to_fbs(self, seed: int | None = None) -> bytes:
    builder = flatbuffers.Builder(0)
    config_t = GenerationConfigurationT()
""")
        to_fbs_return = tab(
            dedent("""
config = config_t.Pack(builder)
builder.Finish(config)
return bytes(builder.Output())
"""),
            1,
        )
        self.to_fbs = tab(to_fbs_def + prop_code + to_fbs_return)

    def save(self, path: str):
        imports = self.gen_imports()
        sections = [
            imports,
            self.config_dict,
            self.class_def,
            self.from_dict,
            self.accessors,
            self.from_json,
            self.to_fbs,
        ]
        sections = [s for s in sections if s is not None]
        _ = open(path, "w").write("\n\n".join(sections))


gen = ConfigCodeGen()
gen.load_props("./resources/config_props.yaml")
gen.gen_dict()
gen.gen_accessors()
gen.gen_from_json()
gen.gen_to_fbs()
gen.save("src/drawthings_py/configs/gen_config_generated.py")
