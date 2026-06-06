from drawthings_py.generated.dt_grpc import config_generated


class GenConfig:
    config_t: config_generated.GenerationConfigurationT

    def __init__(self):
        self.config_t = config_generated.GenerationConfigurationT()

    @property
    def steps(self) -> int:
        return self.config_t.steps

    @steps.setter
    def steps(self, value: int):
        self.config_t.steps = value


gc = GenConfig()
print(vars(gc.config_t))
gc.config_t.steps
