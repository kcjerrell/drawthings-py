"""Configuration management for DrawThings gRPC service.

This module provides utilities for loading and creating configuration dictionaries
from various sources including JSON presets, JSON strings, and Python dictionaries.
"""

import copy
import json
from importlib.resources import files
from typing import Any, Unpack, cast

from .types import ConfigDict
from .presets import PresetName, Presets
from drawthings_py._util import camel_to_snake


config_keymap = {
    "guidance_scale": "guidance",
    "start_width": "width",
    "start_height": "height",
    "hires_fix_start_width": "hires_fix_width",
    "hires_fix_start_height": "hires_fix_height",
    "motion_bucket_id": "motion_scale",
    "cond_aug": "guiding_frame_noise",
    "start_frame_cfg": "start_frame_guidance",
}


def get_field_name(key: str) -> str:
    mapped = config_keymap.get(key, key)
    return camel_to_snake(mapped)


class Configs:
    """Utility class for managing DrawThings service configurations.

    Provides static methods to load configurations from presets, JSON strings,
    or dictionaries, and to create new configuration instances.
    """

    @classmethod
    def from_preset(cls, name: PresetName | Presets) -> ConfigDict:
        """Load a configuration from a named preset.

        Args:
            name: The name of the preset to load. Can be a PresetName enum value
                or a Presets enum value.

        Returns:
            A ConfigDict containing the configuration from the preset.

        Raises:
            ValueError: If the preset file does not exist.
        """
        filename = name + ".json"

        path = files("drawthings_py.configs.json") / filename

        try:
            with path.open("r", encoding="utf-8") as f:
                preset = json.load(f)
                return cls.from_dict(preset["configuration"])
        except FileNotFoundError:
            raise ValueError(f"Unknown preset: {name}")

    @classmethod
    def from_json(cls, data: str) -> ConfigDict:
        """Load a configuration from a JSON string.

        Args:
            data: A JSON string containing configuration data.

        Returns:
            A ConfigDict containing the parsed configuration.
        """
        json_data: dict[str, Any] = json.loads(data)  # pyright: ignore[reportExplicitAny, reportAny]
        snake = {get_field_name(k): v for k, v in json_data.items()}  # type: ignore
        return cls.from_dict(snake)

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],  # pyright: ignore[reportExplicitAny]
    ) -> "ConfigDict":
        """Load a configuration from a dictionary.

        Converts all dictionary keys to snake_case format.

        Args:
            data: A dictionary containing configuration data.

        Returns:
            A ConfigDict with keys converted to snake_case.
        """
        snake = {get_field_name(k): v for k, v in data.items()}  # type: ignore
        d = cast(ConfigDict, snake)  # pyright: ignore[reportInvalidCast]
        return ConfigDict(**d)

    @classmethod
    def create(cls, **kwargs: Unpack[ConfigDict]) -> ConfigDict:
        """Create a new configuration instance.

        Args:
            data: Optional configuration data. If None, creates an empty ConfigDict.

        Returns:
            A new ConfigDict instance.
        """
        return kwargs

    @classmethod
    def combine(cls, *configs: ConfigDict | None):
        """
        Configs are combined in reversed order. The first config will have precedence
        """
        d: ConfigDict = {}
        for config in reversed(configs):
            if config is None:
                continue
            config_copy = copy.deepcopy(config)
            d.update(config_copy)
        return ConfigDict(**d)
