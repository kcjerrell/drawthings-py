"""Configuration management for DrawThings gRPC service.

This module provides utilities for loading and creating configuration dictionaries
from various sources including JSON presets, JSON strings, and Python dictionaries.
"""

import copy
import json
from importlib.resources import files
from typing import Unpack, cast

from .config_generated import GenConfig
from .config_dict import ConfigDict
from .presets import PresetDefinition, PresetName, Presets
from drawthings_py._util import camel_to_snake
from drawthings_py.configs import config_convert


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
    def from_preset(cls, name: PresetName | Presets) -> GenConfig:
        """Load a configuration from a named preset.

        Args:
            name: The name of the preset to load. Can be a PresetName enum value
                or a Presets enum value.

        Returns:
            A ConfigDict containing the configuration from the preset.

        Raises:
            ValueError: If the preset file does not exist.
        """
        try:
            json_str = cls.get_json(name)
            return config_convert.from_json(json_text=json_str)
        except FileNotFoundError:
            raise ValueError(f"Unknown preset: {name}")

    @classmethod
    def get_json(cls, name: PresetName | Presets) -> str:
        """Get the JSON string for a named preset.

        Args:
            name: The name of the preset to get. Can be a PresetName enum value
                or a Presets enum value.

        Returns:
            A JSON string containing the preset data.
        """
        filename = name + ".json"
        path = files("drawthings_py.configs.json") / filename
        preset: PresetDefinition | None = None
        with path.open("r", encoding="utf-8") as f:
            preset = cast(PresetDefinition | None, json.load(f))
        if preset is None:
            raise ValueError(f"Unknown preset: {name}")
        return json.dumps(preset["configuration"])

    @classmethod
    def from_json(cls, data: str) -> GenConfig:
        """Load a configuration from a JSON string.

        Args:
            data: A JSON string containing configuration data.

        Returns:
            A ConfigDict containing the parsed configuration.
        """
        # return config_convert.from_json(json_text=data)
        return GenConfig.from_json(data)

    @classmethod
    def from_dict(
        cls,
        data: ConfigDict,
    ) -> GenConfig:
        """Load a configuration from a dictionary.

        Converts all dictionary keys to snake_case format.

        Args:
            data: A dictionary containing configuration data.

        Returns:
            A ConfigDict with keys converted to snake_case.
        """
        return GenConfig(**data)

    @classmethod
    def create(cls, **kwargs: Unpack[ConfigDict]) -> GenConfig:
        """Create a new configuration instance.

        Args:
            data: Optional configuration data. If None, creates an empty ConfigDict.

        Returns:
            A new ConfigDict instance.
        """
        return GenConfig(**kwargs)

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
