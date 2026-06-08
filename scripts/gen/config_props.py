# pyright: reportUnknownMemberType=false


import re
from typing import Any, Generic, TypeVar, cast

def pluralize(
    count: int, singular: str | None = None, plural: str | None = None
) -> str:
    """
    count: int - the number of items
    singular: str | None - the singular form of the word
    plural: str | None - the plural form of the word
    return: str - the plural or singular form of the word
    The only required param is count.
    Examples:
        >>> plural(1)
        ''
        >>> plural(2)
        's'
        >>> plural(2, "image")
        'images'
        >>> plural(3, "mouse", "mice")
        'mice'
    """
    is_plural = count != 1
    if singular is not None and plural is not None:
        return plural if is_plural else singular
    if singular is not None:
        return singular + "s" if is_plural else singular
    return "s" if is_plural else ""


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

default_fallbacks = {
    "int": 0,
    "float": 0.0,
    "bool": False,
    "str": ""
}

getter_fns = {
    "upscaler": lambda v: f"UpscalerModel(cast(str, {v})) if {v} is not None else None",
    "seed_mode": lambda v: f"SeedMode(cast(int, {v}))",
    "sampler": lambda v: f"SamplerType(cast(int, {v}))",
    "compression_artifacts": lambda v: f"CompressionMethod(cast(int, {v}))",
}


base_type = None
def base_has_attr(name: str) -> bool:
    global base_type
    if base_type is None:
        from drawthings_py.configs.gen_config_base import GenConfigBase
        base_type = GenConfigBase
    
    return hasattr(base_type, name)

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
        if self.schema.get("unused") or base_has_attr(self.name): 
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
        if self.schema.get("unused") or base_has_attr(self.name):
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
        if base_has_attr(self.name):
            return
        all_names = [self.name, self.fbs_name, *self.json_names]

        # def nest(names: list[str]):
        #     if len(names) == 0:
        #         return "None"

        #     name, *rest = names
        #     fallback = nest(rest)
        #     return f'data.get("{name}", {fallback})'

        # prop_code = f"""if {self.name} := {nest(all_names)}:
        get_expr = ' or '.join([f'data.get("{name}")' for name in all_names])
        prop_code = f"""if {self.name} := {get_expr}:
    config_dict["{self.name}"] = cast({self.schema.get("type")}, {self.name})"""

        code.append(prop_code)
        # if v := data.get("width", data.get("start_width", data.get("startWidth"))):

    def gen_to_fbs(
        self,
        code: list[str],
        props_by_name: dict[str, "ConfigProp[Any]"],
        override_name: str | None,
    ) -> None:
        if self.schema.get("unused") or base_has_attr(self.name):
            return

        ignored_expr = self.ignored_expr(props_by_name)
        value_expr = f"self.{self.name}"
        if override_name == self.name:
            value_expr = (
                f"{override_name} if {override_name} is not None else {value_expr}"
            )
        if unit := self.schema.get("fbs", {}).get("unit"):
            value_expr = f"int(round({value_expr} / {unit}))"

        assignment = f"config_t.{self.config_t_name} = {value_expr}"
        if ignored_expr == "False":
            prop_code = assignment
        else:
            prop_code = f"""if not ({ignored_expr}):
    {assignment}
"""

        code.append(prop_code)

    def ignored_expr(self, props_by_name: dict[str, "ConfigProp[Any]"]) -> str:
        ignored = self.schema.get("ignored", False)
        if isinstance(ignored, bool):
            return repr(ignored)

        ignored = cast(dict[str, Any], ignored)
        subject_name = cast(str, ignored["if"])
        subject_expr = f"self.{subject_name}"
        subject_prop = props_by_name[subject_name]

        if "is_in" in ignored:
            values = cast(list[Any], ignored["is_in"])  # pyright: ignore[reportExplicitAny]
            condition = f"{subject_expr} in {self.enum_list_expr(subject_prop, values)}"
        elif "eq" in ignored:
            value = ignored["eq"]
            condition = f"{subject_expr} == {self.enum_value_expr(subject_prop, value)}"
        else:
            condition = subject_expr

        then_value = repr(self.bool_value(ignored["then"]))
        else_value = repr(self.bool_value(ignored["else"]))
        return f"({then_value} if {condition} else {else_value})"

    def bool_value(self, value: Any) -> bool:  # pyright: ignore[reportExplicitAny]
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            if value == "True":
                return True
            if value == "False":
                return False
        return bool(value)

    def enum_list_expr(
        self,
        prop: "ConfigProp[Any]",
        values: list[Any],  # pyright: ignore[reportExplicitAny]
    ) -> str:
        return (
            "[" + ", ".join(self.enum_value_expr(prop, value) for value in values) + "]"
        )

    def enum_value_expr(
        self,
        prop: "ConfigProp[Any]",
        value: Any,  # pyright: ignore[reportExplicitAny]
    ) -> str:
        if not isinstance(value, str):
            return repr(value)
        if "." in value:
            return value

        prop_type = cast(str, prop.schema.get("type")).replace(" | None", "")
        if prop_type in ["int", "str", "float", "bool"]:
            return repr(value)
        return f"{prop_type}.{value}"

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

    @property
    def type(self) -> str:
        return self.schema.get("type")

    @property
    def proper_type(self) -> str:
        t = self.type
        if t.startswith("list["):
            return "List" + t[5].capitalize() + t[5:-1]
        return t[0].capitalize() + t[1:].replace(" | None", "")

    @property
    def default(self) -> T:
        if self.type.startswith("list"):
            return []
        return self.schema.get("default") or default_fallbacks.get(self.type, None)



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
