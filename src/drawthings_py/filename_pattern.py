import re
import os
from pathlib import Path


def _pattern_to_regex(
    pattern: str, is_batch_pattern: bool
) -> tuple[(re.Pattern[str], int)]:
    """
    Convert pattern → regex
    ### → [0-9]{3,}
    """
    group_name = "batch" if is_batch_pattern else "item"
    if is_batch_pattern:
        batch_pattern, _ = _pattern_to_regex(pattern, False)
        pattern = batch_pattern.pattern.replace("$", "#")
    hashes: list[str] = re.findall(r"(#+)", pattern)
    if len(hashes) > 1:
        raise ValueError("Multiple # blocks are not supported in the pattern")
    hash_len = len(hashes[0])
    rep = re.sub(
        r"#+", lambda m: "(?P<{}>[0-9]{{{},}})".format(group_name, len(m[0])), pattern
    )

    return (re.compile(rep), hash_len)


def _extract_number(match: re.Match[str], group: str) -> int:
    return int(match.group(group))


def _next_batch_pattern(pattern: str, directory: str = "") -> str:  # pyright: ignore[reportUnusedFunction]
    if "$" not in pattern:
        raise ValueError("Pattern must include a $ block for the batch counter")
    if "#" not in pattern:
        raise ValueError("Pattern must include a # block for the item counter")

    folder_path = Path(directory or ".")
    folder_path.mkdir(parents=True, exist_ok=True)

    regex, hash_len = _pattern_to_regex(pattern, True)
    numbers: list[int] = []
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
    return result


def _validate_pattern(pattern: str) -> None:
    placeholders = re.findall(r"#+", pattern)
    if len(placeholders) == 0:
        raise ValueError("Pattern must include a # block for the item counter")
    if len(placeholders) > 1:
        raise ValueError(
            "Pattern must include exactly one # block for the item counter"
        )
    if "/" in pattern:
        raise ValueError(
            "Pattern should represent filename only, and cannot contain '/'"
        )


# first set this up without batch counters
class FilenamePattern:
    """
    A callable for generating safe filenames from a pattern.
    """

    _directory: str
    _pattern: str
    _fn_reg: re.Pattern[str]
    _fn_hash_len: int

    def __init__(self, pattern: str, directory: str):
        """
        Initialize a FilenamePattern instance. Call this instance to return the next unused filename
        Note: this API is likly to change

        Args:
            pattern: The filename pattern to use. Must include a single block of # characters
                to indicate where the item counter should be inserted.
            directory: The directory to search for existing files
        """
        _validate_pattern(pattern)

        self._directory = directory
        self._pattern = pattern
        self._fn_reg, self._fn_hash_len = _pattern_to_regex(self._pattern, False)

    def __call__(self) -> Path:
        folder_path = Path(self._directory)
        folder_path.mkdir(parents=True, exist_ok=True)

        numbers: list[int] = []

        for f in folder_path.iterdir():
            if not f.is_file():
                continue
            m = self._fn_reg.match(f.name)
            if m:
                numbers.append(_extract_number(m, "item"))

        if len(numbers) == 0:
            next_num = 1
        else:
            next_num = max(numbers) + 1

        # width rule: minimum width, expands if needed
        final_width = max(self._fn_hash_len, len(str(next_num)))
        result = re.sub("#+", lambda m: str(next_num).zfill(final_width), self._pattern)
        full_path = folder_path.joinpath(result)

        next_filename = full_path
        fallback_num = 0
        while next_filename.exists():
            fallback_num += 1
            root, ext = os.path.splitext(full_path)
            next_filename = folder_path.joinpath(root + "_" + str(fallback_num) + ext)

        if fallback_num > 0:
            print(
                f"Warning: filename pattern failed to produce an unused filename. A fallback filename {next_filename} was used instead. You should report this."
            )

        return next_filename
