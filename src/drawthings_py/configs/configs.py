"""Configuration management for DrawThings gRPC service.

This module provides utilities for loading and creating configuration dictionaries
from various sources including JSON presets, JSON strings, and Python dictionaries.
"""

import json
from importlib.resources import files
from typing import Any

from drawthings_py.configs.types import ConfigDict
from drawthings_py.configs.json.index import PresetName, Presets
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
        return convert_keys_to_snake(data)  # type: ignore

    @classmethod
    def create(cls, data: ConfigDict | None = None) -> ConfigDict:
        """Create a new configuration instance.

        Args:
            data: Optional configuration data. If None, creates an empty ConfigDict.

        Returns:
            A new ConfigDict instance.
        """
        return ConfigDict(**data) if data is not None else ConfigDict()
