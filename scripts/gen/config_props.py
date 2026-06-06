# pyright: reportUnknownMemberType=false


import re
import subprocess
from typing import Any, Callable, Generic, Literal, TypeVar, cast

from textwrap import dedent, indent

from drawthings_py._util import pluralize
from drawthings_py.configs import SamplerType
from drawthings_py.generated.dt_grpc.config_generated import GenerationConfigurationT


def snake_to_camel(s: str) -> str:
    parts = s.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


version_labels = {
    "v1": "SD",
    "v2": "SD2",
    "kandinsky2.1": "Kandinsky",
    "sdxl_base_v0.9": "SDXL",
    "sdxl_refiner_v0.9": "SDXL",
    "ssd_1b": "SSD",
    "svd_i2v": "SVD",
    "wurstchen_v3.0_stage_c": "Wurstchen",
    "wurstchen_v3.0_stage_b": "Wurstchen",
    "sd3": "SD3",
    "pixart": "Pixart",
    "auraflow": "Auraflow",
    "flux1": "Flux.1",
    "sd3_large": "SD3 Large",
    "hunyuan_video": "Hunyuan Video",
    "wan_v2.1_1.3b": "Wan 2.1",
    "wan_v2.1_14b": "Wan 2.1",
    "wan_v2.2_5b": "Wan 2.2 5b",
    "hidream_i1": "HiDream",
    "qwen_image": "Qwen",
    "z_image": "Z Image",
    "flux2": "Flux.2",
    "flux2_4b": "Flux.2 Klein 4b",
    "flux2_9b": "Flux.2 Klein 9b",
    "ltx2": "LTX2",
    "ltx2.3": "LTX2.3",
    "ltx2_3": "LTX2.3",
    "cosmos2.5_2b": "Cosmos2.5",
    "ernie_image": "Ernie Image",
}


getter_fns = {
    "upscaler": lambda v: f"UpscalerModel(cast(str, {v}))",
    "seed_mode": lambda v: f"SeedMode(cast(int, {v}))",
    "sampler": lambda v: f"SamplerType(cast(int, {v}))",
    "compression_artifacts": lambda v: f"CompressionMethod(cast(int, {v}))",
}


T = TypeVar("T")


class ConfigProp(Generic[T]):
    _name: str
    schema: dict[str, Any]  # pyright: ignore[reportExplicitAny]

    def __init__(self, name: str, schema: dict[str, Any]):  # pyright: ignore[reportExplicitAny]
        self._name = name
        self.schema = schema

    def gen_property(self, code: list[str], imports: set[tuple[str, str]]) -> None:
        """
        Generates the code for this property in the GenConfig class
        """
        if self.schema.get("unused"):
            return

        type_value = cast(str, self.schema.get("type"))
        main_type = type_value.replace(" | None", "")

        if main_type not in ["int", "str", "float", "bool", "str | None"]:
            imports.add((".types", main_type))

        get_value_expr = f"self.config_t.{self.config_t_name}"
        set_value_expr = "value"

        if getter_fn := getter_fns.get(self.name):
            get_value_expr = getter_fn(get_value_expr)
        if unit := self.schema.get("fbs", {}).get("unit"):
            get_value_expr = f"{get_value_expr} * {unit}"
            set_value_expr = f"{set_value_expr} / {unit}"
            if main_type == "int":
                set_value_expr = f"int(round({set_value_expr}))"

        prop_code = f"""                                                                                                     
@property
def {self.name}(self) -> {type_value}:
    \"""{self.desc()}\"""
    return {get_value_expr}
@{self.name}.setter
def {self.name}(self, value: {type_value}):
    self.config_t.{self.config_t_name} = {set_value_expr}
"""
        code.append(prop_code)

    def gen_prop_alt(
        self, code: list[str], init: list[str], imports: set[tuple[str, str | None]]
    ) -> None:
        if self.schema.get("unused"):
            return

        type_value = cast(str, self.schema.get("type"))
        main_type = type_value.replace(" | None", "")

        if main_type not in ["int", "str", "float", "bool"]:
            imports.add((".types", main_type))

        default_value = cast(T | None, self.schema.get("default", f"{main_type}()"))

        get_value_expr = f'self._data.get("{self.name}", {default_value})'
        set_value_expr = "value"

        if getter_fn := getter_fns.get(self.name):
            get_value_expr = getter_fn(get_value_expr)

        prop_code = f"""                                                                                                     
@property
def {self.name}(self) -> {type_value}:
    \"""{self.desc()}\"""
    return {get_value_expr}
@{self.name}.setter
def {self.name}(self, value: {type_value}):
    self._data["{self.name}"] = {set_value_expr}
"""
        code.append(prop_code)

    def gen_from_json(
        self, code: list[str], imports: set[tuple[str, str | None]]
    ) -> None:
        all_names = [self.name, self.fbs_name, *self.json_names]

        def nest(names: list[str]):
            if len(names) == 0:
                return "None"

            name, *rest = names
            fallback = nest(rest)
            return f'data.get("{name}", {fallback})'

        prop_code = f"""
if {self.name} := {nest(all_names)}:
    config_dict["{self.name}"] = {self.name}
"""

        code.append(prop_code)
        # if v := data.get("width", data.get("start_width", data.get("startWidth"))):

    @property
    def name(self) -> str:
        return self._name

    @property
    def fbs_name(self) -> str:
        fbs = cast(dict[str, str], self.schema.get("fbs", {}))
        return fbs.get("name", self.name)

    @property
    def json_names(self) -> list[str]:
        if json_names := cast(str | list[str], self.schema.get("json")):
            if isinstance(json_names, str):
                return [json_names]
            return json_names
        return []

    @property
    def config_t_name(self) -> str:
        return snake_to_camel(self.fbs_name)

    def desc(self) -> str:
        desc = self.schema.get("description", self._name)
        if versions := self.schema.get("versions"):
            labels = [version_labels.get(v) for v in versions]
            if None in labels:
                raise ValueError(f"Unknown version: {versions}")
            version_text = (
                f" Used with model version{pluralize(len(labels))} {', '.join(labels)}"
            )
            version_text = re.sub(r",([^,]+)$", r" and\1", version_text)
            desc += version_text
        return desc


# props_codes: list[str] = []
# imports: set[tuple[str, str]] = set()
# imports.add(("drawthings_py.generated.dt_grpc", "config_generated"))
# imports.add(("drawthings_py.configs.types", "ConfigDict"))
# imports.add(("typing", "cast"))
# imports.add(("typing", "Any"))

# for prop in props:
#     prop.gen_prop_alt(props_codes, [], imports)


# imports_modules: dict[str, list[str]] = {}
# for im_module, im_name in imports:
#     if im_module not in imports_modules:
#         imports_modules[im_module] = []
#     imports_modules[im_module].append(im_name)

# imports_code = "\n".join(
#     [
#         f"from {im_module} import {', '.join(im_names)}"
#         for im_module, im_names in imports_modules.items()
#     ]
# )

# code = "\n\n".join([imports_code, class_def, tab("\n".join(props_codes), 1)])

# _ = open("./src/drawthings_py/configs/gen_config_generated.py", "w").write(code)

# _ = subprocess.run(
#     ["ruff", "format", "./src/drawthings_py/configs/gen_config_generated.py"]
# )
