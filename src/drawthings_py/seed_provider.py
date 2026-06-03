from random import Random


class SeedProvider:
    """
    A provider for generating random seeds.
    """

    rand: Random
    index_seeds: dict[int, int]

    def __init__(self, x: str | int | float | bytes | None = None):
        self.rand = Random(x)
        self.index_seeds = {}

    def get_seed(self, n: int | None):
        if n == -1 or n == 0 or n is None:
            return self.rand.randint(0, 2**32 - 1)
        if n > 0:
            return n
        if n not in self.index_seeds:
            self.index_seeds[n] = self.rand.randint(0, 2**32 - 1)
        return self.index_seeds[n]
