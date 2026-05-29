import json
from importlib.resources import files

from drawthings_py.configs import ConfigDict
from drawthings_py.configs.json.index import PresetName, Presets


class Configs:
    @classmethod
    def from_preset(cls, name: PresetName | Presets) -> ConfigDict:
      filename = name + ".json"

      path = files("drawthings_py.configs.json") / filename

      try:
          with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
            return ConfigDict.from_dict(data["configuration"])
      except FileNotFoundError:
        raise ValueError(f"Unknown preset: {name}")

      return cls(**data)

    @classmethod
    def from_json(cls, data: str) -> ConfigDict:
      json_data = json.loads(data)
      return ConfigDict.from_dict(json_data)

    @classmethod  
    def create(cls, data: ConfigDict | None = None) -> ConfigDict:
      return ConfigDict(data) if data is not None else ConfigDict()