import os
import sys
from pathlib import Path
import pytest


# Ensure `src` is importable when running tests from the project root
SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from drawthings_py._util import next_filename, next_batch_pattern
from drawthings_py._util import seeds_from_batch


def test_next_filename_empty_dir(tmp_path):
    pattern = "output_####.png"
    result = next_filename(pattern, str(tmp_path))
    assert os.path.basename(result) == "output_0001.png"


def test_next_filename_existing_match(tmp_path):
    (tmp_path / "output_0002.png").write_text("")
    pattern = "output_####.png"
    result = next_filename(pattern, str(tmp_path))
    assert os.path.basename(result) == "output_0003.png"


def test_next_filename_nonmatching_existing(tmp_path):
    # a file that doesn't match the #### block should be ignored
    (tmp_path / "output_2.png").write_text("")
    pattern = "output_####.png"
    result = next_filename(pattern, str(tmp_path))
    assert os.path.basename(result) == "output_0001.png"


def test_next_filename_expand_width(tmp_path):
    # when highest matching value would overflow the original width
    (tmp_path / "output_9999.png").write_text("")
    pattern = "output_####.png"
    result = next_filename(pattern, str(tmp_path))
    assert os.path.basename(result) == "output_10000.png"


def test_next_filename_fallback(tmp_path, capsys):
    # force the initially generated filename to already exist to trigger fallback
    # if output_0001 exists the function should return the next sequential
    # filename (output_0002.png)
    (tmp_path / "output_0001.png").write_text("")
    pattern = "output_####.png"
    result = next_filename(pattern, str(tmp_path))
    assert os.path.basename(result) == "output_0002.png"


def test_next_batch_pattern_empty_dir(tmp_path):
    pattern = "sd_$$_#####.png"
    result = next_batch_pattern(pattern, str(tmp_path))
    assert result == os.path.join(tmp_path, "sd_01_#####.png")


def test_next_batch_pattern_existing_batches(tmp_path):
    (tmp_path / "sd_01_00001.png").write_text("")
    (tmp_path / "sd_02_00001.png").write_text("")
    pattern = "sd_$$_#####.png"
    result = next_batch_pattern(pattern, str(tmp_path))
    assert result == os.path.join(tmp_path, "sd_03_#####.png")


def test_next_filename_invalid_patterns(tmp_path):
    # no # block
    with pytest.raises(ValueError):
        next_filename("my_image.png", str(tmp_path))

    # multiple # blocks
    with pytest.raises(ValueError):
        next_filename("###_numbers_###.yay", str(tmp_path))


def test_next_batch_pattern_invalid_patterns(tmp_path):
    # no $ block
    with pytest.raises(ValueError):
        next_batch_pattern("batch_4_image_##.png", str(tmp_path))

    # no # block
    with pytest.raises(ValueError):
        next_batch_pattern("batch_$_image_02.png", str(tmp_path))

    # multiple $ blocks (should be rejected)
    with pytest.raises(ValueError):
        next_batch_pattern("bb_$$_bb_$$_##.png", str(tmp_path))

    # multiple # blocks
    with pytest.raises(ValueError):
        next_batch_pattern("b_$$_img_##_##.png", str(tmp_path))


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


def test_next_batch_pattern_with_next_filename(tmp_path):
    pattern = "sd_$$_##.png"
    (tmp_path / "sd_01_01.png").write_text("")

    batch_pattern = next_batch_pattern(pattern, str(tmp_path))
    assert batch_pattern == os.path.join(tmp_path, "sd_02_##.png")

    f1 = next_filename(batch_pattern)
    assert os.path.basename(f1) == "sd_02_01.png"
    assert os.path.dirname(f1) == str(tmp_path)
    Path(f1).write_text("")

    f2 = next_filename(batch_pattern)
    assert os.path.basename(f2) == "sd_02_02.png"
    Path(f2).write_text("")

    f3 = next_filename(batch_pattern)
    assert os.path.basename(f3) == "sd_02_03.png"

    batch_pattern = next_batch_pattern(pattern, str(tmp_path))
    assert batch_pattern == os.path.join(tmp_path, "sd_03_##.png")

    f4 = next_filename(batch_pattern)
    assert os.path.basename(f4) == "sd_03_01.png"
    