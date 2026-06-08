from __future__ import annotations
from typing import Unpack

from drawthings_py.configs.config_dict import ConfigDict
from drawthings_py.configs.types import LoraDict


class GenConfigBase:
    _data: ConfigDict

    def __init__(self, **kwargs: Unpack[ConfigDict]):
        self._data = ConfigDict(**kwargs)
        self._loras: list[LoraDict] = []

    @property
    def seed(self) -> int:
        return self._data.get("seed", -1)

    @seed.setter
    def seed(self, value: int):
        self._data["seed"] = value

    @property
    def loras(self) -> list[LoraDict]:
        return self._loras

    @loras.setter
    def loras(self, value: list[LoraDict]):
        self._loras = value

    @classmethod
    def from_dict(cls, data: ConfigDict):
        return cls(**data)

    def update(self, data: ConfigDict):
        self._data.update(data)

    @classmethod
    def _apply_json(
        cls,
        config: GenConfigBase,
        json_text: str | None = None,
        json_data: ConfigDict | None = None,
    ):
        pass
