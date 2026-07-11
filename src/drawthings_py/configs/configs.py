"""Configuration management for DrawThings gRPC service.

This module provides utilities for loading and creating configs from various sources
including JSON presets, JSON strings, and Python dictionaries.
"""

import copy
from typing import Unpack

from .gen_config import GenConfig
from .config_dict import ConfigDict
from .presets import PresetName, Presets, load_preset_config


class Configs:
    """Utility class for managing GenConfigs - Draw Things's image generation
    configuration.

    Provides static methods to load, create, and merge configs.
    """

    @classmethod
    def from_preset(cls, name: PresetName | Presets) -> GenConfig:
        """Load a config from a community preset.

        Args:
            name: The name of the preset to load.

        Returns:
            A GenConfig containing the configuration from the preset.

        Raises:
            ValueError: If the preset file does not exist.
        """
        try:
            json_str = load_preset_config(name)
            return GenConfig.from_json(json_str)
        except FileNotFoundError:
            raise ValueError(f"Unknown preset: {name}")

    @classmethod
    def from_json(cls, data: str) -> GenConfig:
        """Load a configuration from a JSON string.

        Args:
            data: A JSON string containing configuration data.

        Returns:
            A GenConfig containing the config
        """
        return GenConfig.from_json(data)

    @classmethod
    def create(
        cls, config: ConfigDict | None = None, /, **kwargs: Unpack[ConfigDict]
    ) -> GenConfig:
        """Create a new configuration with keyword arguments or a dictionary

        config = Configs.create(width=768, height=768, ...)
        config = Configs.create({
            "width": 768,
            "height": 768,
            ...
        })

        Args:
            kwargs: Configuration parameters to set.

        Returns:
            A new GenConfig instance.
        """
        return GenConfig(**(config or {}) | kwargs)

    @classmethod
    def combine(cls, *configs: ConfigDict | GenConfig | None) -> GenConfig:
        """
        Configs are combined in reversed order. The first config will have precedence
        """
        copies = [
            copy.deepcopy(config._d)  # pyright: ignore[reportPrivateUsage]
            if isinstance(config, GenConfig)
            else copy.deepcopy(config)
            for config in configs
            if config is not None
        ]
        d: ConfigDict = {}
        for config_copy in reversed(copies):
            d.update(config_copy)
        return GenConfig(**d)
