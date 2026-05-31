import os
import sys
from pathlib import Path
import pytest


# Ensure `src` is importable when running tests from the project root
SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from drawthings_py._util import next_filename, next_batch_pattern
from drawthings_py._util import seeds_from_batch

def test_seeds_from_batch_examples():
    # example 1
    init = 1000
    size = 4
    expected = [1000, 266172694, 3204629577, 385443340]
    assert seeds_from_batch(init, size, 2) == expected

    # example 2
    init = 99999999
    size = 4
    expected = [99999999, 2225200458, 1578146574, 3814640502]
    assert seeds_from_batch(init, size, 2) == expected
    
    init = 555
    size = 4
    expected = [555, 555, 555, 555]
    assert seeds_from_batch(init, size, 0) == expected