"""
Utility functions for DrawThings Py
"""

import re
from random import randint


def pluralize(
    count: int, singular: str | None = None, plural: str | None = None
) -> str:
    """
    count: int - the number of items
    singular: str | None - the singular form of the word
    plural: str | None - the plural form of the word
    return: str - the plural or singular form of the word
    The only required param is count.
    Examples:
        >>> plural(1)
        ''
        >>> plural(2)
        's'
        >>> plural(2, "image")
        'images'
        >>> plural(3, "mouse", "mice")
        'mice'
    """
    is_plural = count != 1
    if singular is not None and plural is not None:
        return plural if is_plural else singular
    if singular is not None:
        return singular + "s" if is_plural else singular
    return "s" if is_plural else ""


def seeds_from_batch(init: int, size: int, seed_mode: int) -> list[int]:
    """
    Given the initial seed and a batch size, will return a list of uint32 seeds of length size, including the init_seed
    This series will match the seeds used by draw things when using a batch size
    """
    if seed_mode == 0 and size > 1:
        print(
            "Warning: Legacy seed mode is not fully supported. Any images in a batch larger than 1 will have incorrect seed in their metadata"
        )

    if seed_mode > 3 and size > 1:
        print(
            "Warning: Unknown seed mode {} may not be supported. Any images in a batch larger than 1 may have incorrect seed in their metadata".format(
                seed_mode
            )
        )

    # legacy, torch, nvidia, or unknown
    if seed_mode != 2:
        return [init] * size

    # scale alike
    seeds = [init]
    for _ in range(size - 1):
        seeds.append(xorshift(seeds[-1]))
    return seeds


def xorshift(a: int) -> int:
    """
    XORShift random number generator
    Match Swift's UInt32 behavior
    """
    x = 0x0BAD5EED if a == 0 else a
    x &= 0xFFFFFFFF
    x ^= (x << 13) & 0xFFFFFFFF
    x ^= x >> 17
    x ^= (x << 5) & 0xFFFFFFFF
    return x & 0xFFFFFFFF


def random_seed() -> int:
    """
    Returns a random seed value between 0 and 2^32 - 1
    """
    return randint(0, 2**32 - 1)


def camel_to_snake(name: str) -> str:
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def snake_to_camel(s: str) -> str:
    parts = s.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])
