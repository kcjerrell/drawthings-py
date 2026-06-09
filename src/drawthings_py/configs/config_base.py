from typing import Unpack
from drawthings_py.configs.config_dict import ConfigDict


class GenConfigBase:
    _d: ConfigDict

    def __init__(self, **kwargs: Unpack[ConfigDict]):
        self._d = ConfigDict(**kwargs)
