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

T = TypeVar("T")


class ConfigProp(Generic[T]):
    """Represents a GenConfig property during code generation. Used to load the yaml
    specification and provide data for the jinja template"""
    _name: str
    schema: dict[str, Any]  # pyright: ignore[reportExplicitAny]

    def __init__(self, name: str, schema: dict[str, Any]):  # pyright: ignore[reportExplicitAny]
        self._name = name
        self.schema = schema

    @property
    def name(self) -> str:
        """the property's python name in GenConfig"""
        return self._name

    @property
    def fbs_name(self) -> str:
        """the property's name in the flatbuffer"""
        fbs = cast(dict[str, str], self.schema.get("fbs", {}))
        return fbs.get("name", self.name)

    def get_desc(self, include_versions: bool = False) -> str:
        desc = self.schema.get("description", self._name)
        if self.schema.get("unused"):
            desc = "Unused. " + desc
        if include_versions and (versions := self.schema.get("versions")):
            labels = [version_labels.get(v) for v in versions]
            if None in labels:
                raise ValueError(f"Unknown version: {versions}")
            version_text = (
                f". Used with model version{pluralize(len(labels))} {', '.join(labels)}"
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

    @property
    def unused(self) -> bool:
        return self.schema.get("unused", False)