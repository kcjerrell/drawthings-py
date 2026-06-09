import json
import re
import subprocess
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

from jinja2 import Environment, FileSystemLoader, select_autoescape
env = Environment(
    loader=FileSystemLoader("./scripts/gen"),
    autoescape=select_autoescape(),
    trim_blocks=True,
    lstrip_blocks=True,
)

config_dict_names = {
    'all': "Gen",
    'core': 'Core',
    'extra': 'Extra',
    'hires_fix': 'HiResFix',
    'upscaler': 'Upscaler',
    'refiner': 'Refiner',
    'hidream_i1': 'HiDream',
    'v1': 'SD1And2',
    'v2': 'SD1And2',
    'sdxl_base_v0.9': 'SDXL',
    'sdxl_refiner_v0.9': 'SDXL',
    'flux1': 'Flux',
    'pixart': None,
    'sd3': 'SD3',
    'sd3_large': 'SD3',
    'ssd_1b': None,
    'svd_i2v': 'SVD',
    'hunyuan_video': 'Hunyuan',
    'ltx2': 'LTX2',
    'wan_v2.1_1.3b': 'Wan',
    'wan_v2.1_14b': 'Wan',
    'wan_v2.2_5b': 'Wan5b',
    'tiled': 'Tiled',
    'flux2': 'Flux2',
    'flux2_4b': 'Flux2Klein',
    'flux2_9b': 'Flux2Klein',
    'qwen_image': 'QwenImage',
    'z_image': 'ZImage',
    'cosmos2.5_2b': 'Anima',
    'auraflow': 'AuraFlow',
    'ernie_image': 'ErnieImage'
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
    imports: ImportsBuilder
    all_types: set[str]

    def __init__(self):
        self.props = []
        self.imports = ImportsBuilder()
        self.all_types = set()

    def load_props(self):
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

        for prop in self.props:
            t = prop.type.replace(" | None", "")
            self.all_types.add(t)
            if t not in ['str', 'int', 'float', 'bool']:
                self.imports.add("drawthings_py.configs.types", t)

    def group_props(self, group_versions: bool):
        groups: dict[str, object] = {}


        def add(dict_name: str, prop: ConfigProp[object]):
            nonlocal groups
            group_name = config_dict_names[dict_name]
            if group_name is None:
                return
            if group_name not in groups:
                groups[group_name] = { "types": {}, "props": [] }

            groups[group_name]["props"].append(prop)

            if prop.proper_type not in groups[group_name]["types"]:
                groups[group_name]["types"][prop.proper_type] = []
            groups[group_name]["types"][prop.proper_type].append(prop)

        for prop in self.props: 
            add("all", prop)
            if group := cast(str | None, prop.schema.get("group")):
                add(group, prop)
            if group_versions and (versions := cast(list[str] | None, prop.schema.get("versions"))):
                for version in versions:
                    add(version, prop)

        return groups, sorted(self.all_types)

gen = ConfigCodeGen()
gen.load_props()
imports = gen.imports.build()
groups, all_types = gen.group_props(False)

props_by_name = {prop.name: prop for prop in gen.props}
context = dict(groups=groups, imports=imports, all_types=all_types, include_groups=["Core"], all_props=gen.props, props_by_name=props_by_name)

# Generate config_dict.py
config_dict_template = env.get_template("config_dict.py.jinja")
config_dict_code = config_dict_template.render(**context)
open("./src/drawthings_py/configs/config_dict.py", "w").write(config_dict_code)
_ = subprocess.run(
    ["ruff", "format", "./src/drawthings_py/configs/config_dict.py"]
)

# Generate config_base_generated.py
template = env.get_template("config_convert.py.jinja")
code = template.render(**context)

open("./src/drawthings_py/configs/config_convert.py", "w").write(code)
_ = subprocess.run(
    ["ruff", "format", "./src/drawthings_py/configs/config_base.py"]
)

# Generate config_generated.py
template = env.get_template("config_generated.py.jinja")
code = template.render(**context)

open("./src/drawthings_py/configs/config_generated.py", "w").write(code)
_ = subprocess.run(
    ["ruff", "format", "./src/drawthings_py/configs/config_generated.py"]
)

# _ = open("temp.json", "w").write(json.dumps(context, default=lambda o: [p for p in dir(o) if not p.startswith("_")]))