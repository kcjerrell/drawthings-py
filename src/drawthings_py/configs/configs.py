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
from drawthings_py._util import convert_keys_to_snake


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
                data = json.load(f)
                return cls.from_dict(data["configuration"])
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
        json_data = json.loads(data)
        return cls.from_dict(json_data)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ConfigDict":
        """Load a configuration from a dictionary.

        Converts all dictionary keys to snake_case format.

        Args:
            data: A dictionary containing configuration data.

        Returns:
            A ConfigDict with keys converted to snake_case.
        """
        snake = convert_keys_to_snake(data)  # type: ignore
        return ConfigDict(**snake)

    @classmethod
    def create(cls, **kwargs: Unpack[ConfigDict]) -> ConfigDict:
        """Create a new configuration instance.

        Args:
            data: Optional configuration data. If None, creates an empty ConfigDict.

        Returns:
            A new ConfigDict instance.
        """
        return cast(ConfigDict, kwargs)

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
