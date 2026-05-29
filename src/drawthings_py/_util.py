import os
from pathlib import Path
from random import randint
import re
from typing import Tuple, List, Optional


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


# filename pattern
# output_####.png - replaced with 4+ digits incrementing. always uses the +1 from
#    the highest matching filename. will use additional digits if necessary,
# .   the number of digits is a minimum

# .   output_2 exists and pattern is output_####
# .     in this case, the file would be output_0001, because output_2 doesn't
# .     match the pattern
# .   output_0002 exists and pattern is output_####
# .     in this case, the file would be output_0003, because output_0002 matches
# .     the pattern
# .   output_9999 exists and pattern is output_####
# .     in this case, the file would be output_10000
# .   output_10000 exists and pattern is output_####
# .     in this case, the file would be output_10001, because output_10000 matches
# .     the pattern.
# .   output_001 exists and output_005. the pattern is output_###<
# .     in this case, the file should be output_002.
# .     the < modiifer on the pattern indicates that the lowest possible value
# .     should be used (as opposed to the max + 1)
# image.png


def _find_counter(pattern: str) -> Tuple[str, int]:
    """
    Returns (hash_block, width)
    """
    m = re.search(r"(#+)", pattern)
    if not m:
        return "", 0
    return m.group(1), len(m.group(1))


def _pattern_to_regex(pattern: str, is_batch_pattern: bool) -> tuple[(re.Pattern, int)]:
    """
    Convert pattern → regex
    ### → [0-9]{3,}
    """
    group_name = "batch" if is_batch_pattern else "item"
    if is_batch_pattern: 
        batch_pattern, _ = _pattern_to_regex(pattern, False)
        pattern = batch_pattern.pattern.replace("$", "#")
    hashes = re.findall(r"(#+)", pattern)
    if len(hashes) > 1:
        raise ValueError("Multiple # blocks are not supported in the pattern")
    hash_len = len(hashes[0])
    rep = re.sub(r"#+", lambda m: "(?P<{}>[0-9]{{{},}})".format(group_name, len(m[0])), pattern)
    
    return (re.compile(rep), hash_len)


def _extract_number(match: re.Match, group: str) -> int:
    return int(match.group(group))


def next_filename(pattern: str, directory: str | None = None) -> str:
    if "#" not in pattern:
        raise ValueError("Pattern must include a # block for the item counter")
    
    # the pattern might include a directory (esp if used with batch pattern)
    # we need to join the pattern and the directory to get the folder to search in
    dir_name = Path(os.path.dirname(pattern))
    folder_path = Path(directory or ".").joinpath(dir_name)
    folder_path.mkdir(parents=True, exist_ok=True)

    regex, hash_len = _pattern_to_regex(os.path.basename(pattern), False)
    numbers: List[int] = []
    for f in folder_path.iterdir():
        if not f.is_file():
            continue
        m = regex.match(f.name)
        if m:
            numbers.append(_extract_number(m, "item"))
    # decide next value
    if not numbers:
        next_num = 1
    else:
        next_num = max(numbers) + 1
    # width rule: minimum width, expands if needed
    final_width = max(hash_len, len(str(next_num)))
    result = re.sub("#+", lambda m: str(next_num).zfill(final_width), pattern)
    full_path = os.path.join(folder_path, result)
    
    next_filename = full_path
    fallback_num = 0
    while os.path.exists(next_filename):
        root, ext = os.path.splitext(full_path)
        next_filename = root + "_" + str(fallback_num) + ext
        fallback_num += 1
    
    if fallback_num > 0:
        print(f"Warning: filename pattern failed to produce an unused filename. A fallback filename {next_filename} was used instead. You should report this.")
    
    return next_filename


def next_batch_pattern(pattern: str, directory: str = "") -> str:
    if "$" not in pattern:
        raise ValueError("Pattern must include a $ block for the batch counter")
    if "#" not in pattern:
        raise ValueError("Pattern must include a # block for the item counter")
    
    folder_path = Path(directory or ".")
    folder_path.mkdir(parents=True, exist_ok=True)

    regex, hash_len = _pattern_to_regex(pattern, True)
    numbers: List[int] = []
    for f in folder_path.iterdir():
        if not f.is_file():
            continue
        m = regex.match(f.name)
        if m:
            numbers.append(_extract_number(m, "batch"))
    # decide next value
    if not numbers:
        next_num = 1
    else:
        next_num = max(numbers) + 1
    # width rule: minimum width, expands if needed
    final_width = max(hash_len, len(str(next_num)))
    result = re.sub("\\$+", lambda m: str(next_num).zfill(final_width), pattern)
    return os.path.join(folder_path, result)


def seeds_from_batch(init: int, size: int, seed_mode: int) -> list[int]:
    """
    Given the initial seed and a batch size, will return a list of uint32 seeds of length size, including the init_seed
    This series will match the seeds used by draw things when using a batch size
    """
    if seed_mode == 0 and size > 1:
        print("Warning: Legacy seed mode is not fully supported. Any images in a batch larger than 1 will have incorrect seed in their metadata")
    
    if seed_mode > 3 and size > 1:
        print("Warning: Unknown seed mode {} may not be supported. Any images in a batch larger than 1 may have incorrect seed in their metadata".format(seed_mode))
    
    # legacy, torch, nvidia, or unknown
    if seed_mode != 2:
        return [init] * size
    
    # scale alike    
    seeds = [init]
    for i in range(size - 1):
        seeds.append(xorshift(seeds[-1]))
    return seeds

def xorshift(a: int) -> int:
    # match Swift's UInt32 behavior
    x = 0x0BAD5EED if a == 0 else a
    x &= 0xFFFFFFFF
    x ^= (x << 13) & 0xFFFFFFFF
    x ^= (x >> 17)
    x ^= (x << 5) & 0xFFFFFFFF
    return x & 0xFFFFFFFF

def get_seed() -> int:
    return randint(0, 2**32 - 1)