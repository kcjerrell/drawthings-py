import re
from textwrap import dedent, indent
from typing import cast

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

config_dict_names = {
    'all': "ConfigDict",
    'core': 'CoreConfig',
    'extra': 'ExtraConfig',
    'hires_fix': 'HiResFixConfig',
    'upscaler': 'UpscalerConfig',
    'refiner': 'RefinerConfig',
    'hidream_i1': 'HiDreamConfig',
    'v1': 'SD1And2Config',
    'v2': 'SD1And2Config',
    'sdxl_base_v0.9': 'SDXLConfig',
    'sdxl_refiner_v0.9': 'SDXLConfig',
    'flux1': 'FluxConfig',
    'pixart': None,
    'sd3': 'SD3Config',
    'sd3_large': 'SD3Config',
    'ssd_1b': None,
    'svd_i2v': 'SVDConfig',
    'hunyuan_video': 'HunyuanConfig',
    'ltx2': 'LTX2Config',
    'wan_v2.1_1.3b': 'WanConfig',
    'wan_v2.1_14b': 'WanConfig',
    'wan_v2.2_5b': 'Wan5bConfig',
    'tiled': 'TiledConfig',
    'flux2': 'Flux2Config',
    'flux2_4b': 'Flux2KleinConfig',
    'flux2_9b': 'Flux2KleinConfig',
    'qwen_image': 'QwenImageConfig',
    'z_image': 'ZImageConfig',
    'cosmos2.5_2b': 'AnimaConfig',
    'auraflow': 'AuraFlowConfig',
    'ernie_image': 'ErnieImageConfig'
}


def tab(text: str, level: int = 1) -> str:
    return indent(text, "    " * level)

class ImportsBuilder:
    imports: set[tuple[str, str | None]]

    def __init__(self):
        self.imports = set()

    def add(self, module: str, name: str | None = None):
        self.imports.add((module, name))

    def build(self) -> str:
        imports_modules: dict[str, list[str] | None] = {}
        for im_module, im_name in self.imports:
            if im_module not in imports_modules:
                imports_modules[im_module] = [] if im_name is not None else None
            if im_name is not None:
                if im_name.startswith("list["):
                    im_name = im_name[5:-1]
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
class GenConfig(GenConfigBase):
    _data: ConfigDict

    def __init__(self, **kwargs: Unpack[ConfigDict]):
        super().__init__(**kwargs)
                """
        self.imports.add(("typing", "Unpack"))
        self.imports.add(("drawthings_py.configs.gen_config_base", "GenConfigBase"))

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
                Optional("gen_ignore"): Bool(),
                Optional("group"): Str()
            }
        )
        schema = MapPattern(Str(), property_schema)
        json_text = open("./resources/config_props.yaml", "r").read()
        yaml = load(json_text, schema)
        print(yaml.is_mapping())
        props_yaml = yaml.data
        self.props = [ConfigProp(key, value) for key, value in props_yaml.items()]

    def gen_dicts(self):
        imports = ImportsBuilder()
        imports.add("typing", "TypedDict")
        dicts: dict[str, set[str]] = {}

        def add(dict_name: str, desc: str, definition: str):
            nonlocal dicts
            class_name = config_dict_names[dict_name]
            if class_name is None:
                return
            if class_name not in dicts:
                dicts[class_name] = set()
            dicts[class_name].add(definition + "\n" + desc)
 
        for prop in self.props:
            prop_type: str = prop.schema.get("type")
            desc = f'"""{prop.desc()}"""'
            definition = f"{prop.name}: {prop_type}"

            if prop_type.replace(" | None", "") not in ["str", "int", "float", "bool"]:
                imports.add(".types", prop_type.replace(" | None", ""))

            add("all", desc, definition)
            if group := cast(str | None, prop.schema.get("group")):
                add(group, desc, definition)
            if versions := cast(list[str] | None, prop.schema.get("versions")):
                for version in versions:
                    add(version, desc, definition)

        classes: list[str] = []
        bodies: dict[str, list[str]] = {}

        for key, lines in dicts.items():
            class_name = re.sub(r"[._]", "", key)
            class_def = f"""class {class_name}(TypedDict, total=False):\n"""
            body = tab("\n".join(lines), 1)
            classes.append(class_def + body)

            if body not in bodies:
                bodies[body] = []
            bodies[body].append(class_name)

        print(bodies.values())
        print(dicts.keys())
        
        imports_code = imports.build() 

        code = "\n\n".join([imports_code, *classes])
        open("./src/drawthings_py/configs/config_dict.py", "w").write(code)

    def gen_imports(self):
        self.imports.add(("typing", "cast"))

        imports_modules: dict[str, list[str] | None] = {}
        for im_module, im_name in self.imports:
            if im_module not in imports_modules:
                imports_modules[im_module] = [] if im_name is not None else None
            if im_name is not None:
                if im_name.startswith("list["):
                    im_name = im_name[5:-1]
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
        from_json_return = tab("""
config = GenConfig.from_dict(config_dict)
GenConfigBase._apply_json(config, json_text=json_text, json_data=json_data)
return config""", 1)
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
            self.class_def,
            self.accessors,
            self.from_json,
            self.to_fbs,
        ]
        sections = [s for s in sections if s is not None]
        _ = open(path, "w").write("\n\n".join(sections))


gen = ConfigCodeGen()
gen.load_props("./resources/config_props.yaml")
gen.gen_dicts()
gen.gen_accessors()
gen.gen_from_json()
gen.gen_to_fbs()
gen.save("src/drawthings_py/configs/gen_config_generated.py")
