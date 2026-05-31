"""
Tests for FilenamePattern
"""
import pytest
from pathlib import Path
from drawthings_py import FilenamePattern


def test_next_filename_empty_dir(tmp_path):
    """in an empty directory, filename starts at 0001"""
    next_filename = FilenamePattern("output_####.png", tmp_path)
    result = next_filename()
    assert result == Path(tmp_path, "output_0001.png")


def test_next_filename_existing_match(tmp_path):
    """if there is matching file, next file name will be the max match + 1"""
    (tmp_path / "output_0002.png").write_text("")
    next_filename = FilenamePattern("output_####.png", tmp_path)
    result = next_filename()
    assert result == Path(tmp_path, "output_0003.png")


def test_next_filename_nonmatching_existing(tmp_path):
    """a file that doesn't have at least 4 digits doesn't match the pattern"""
    (tmp_path / "output_2.png").write_text("")
    next_filename = FilenamePattern("output_####.png", tmp_path)
    result = next_filename()
    assert result == Path(tmp_path, "output_0001.png")


def test_next_filename_expand_width(tmp_path):
    """more digits will be used if needed"""
    (tmp_path / "output_9999.png").touch()
    next_filename = FilenamePattern("output_####.png", tmp_path)
    result = next_filename()
    assert result == Path(tmp_path, "output_10000.png")


# def test_next_batch_pattern_empty_dir(tmp_path):
#     pattern = "sd_$$_#####.png"
#     result = next_batch_pattern(pattern, str(tmp_path))
#     assert result == os.path.join(tmp_path, "sd_01_#####.png")


# def test_next_batch_pattern_existing_batches(tmp_path):
#     (tmp_path / "sd_01_00001.png").write_text("")
#     (tmp_path / "sd_02_00001.png").write_text("")
#     pattern = "sd_$$_#####.png"
#     result = next_batch_pattern(pattern, str(tmp_path))
#     assert result == os.path.join(tmp_path, "sd_03_#####.png")


def test_next_filename_invalid_patterns(tmp_path):
    """invalid patterns raise ValueError"""
    with pytest.raises(ValueError):
        next_filename = FilenamePattern("image.png", tmp_path)
        next_filename()

    # multiple # blocks
    with pytest.raises(ValueError):
        next_filename = FilenamePattern("image_##_##.png", tmp_path)

def test_two(tmp_path):
    """Two patterns should not interfere with each other"""
    next_filename_a = FilenamePattern("image_##.png", tmp_path)
    next_filename_b = FilenamePattern("image_##.png", tmp_path)

    assert len([f for f in Path.iterdir(tmp_path)]) == 0

    next_filename_a().touch()
    next_filename_a().touch()

    next_a = next_filename_a()
    assert next_a == Path(tmp_path, "image_03.png")
    next_b = next_filename_b()
    assert next_b == Path(tmp_path, "image_03.png")

    next_filename_b().touch()

    next_a = next_filename_a()
    assert next_a == Path(tmp_path, "image_04.png")

    assert len([f for f in Path.iterdir(tmp_path)]) == 3



# def test_next_batch_pattern_invalid_patterns(tmp_path):
#     # no $ block
#     with pytest.raises(ValueError):
#         next_batch_pattern("batch_4_image_##.png", str(tmp_path))

#     # no # block
#     with pytest.raises(ValueError):
#         next_batch_pattern("batch_$_image_02.png", str(tmp_path))

#     # multiple $ blocks (should be rejected)
#     with pytest.raises(ValueError):
#         next_batch_pattern("bb_$$_bb_$$_##.png", str(tmp_path))

#     # multiple # blocks
#     with pytest.raises(ValueError):
#         next_batch_pattern("b_$$_img_##_##.png", str(tmp_path))


# def test_next_batch_pattern_with_next_filename(tmp_path):
#     pattern = "sd_$$_##.png"
#     (tmp_path / "sd_01_01.png").write_text("")

#     batch_pattern = next_batch_pattern(pattern, str(tmp_path))
#     assert batch_pattern == os.path.join(tmp_path, "sd_02_##.png")

#     f1 = next_filename(batch_pattern)
#     assert os.path.basename(f1) == "sd_02_01.png"
#     assert os.path.dirname(f1) == str(tmp_path)
#     Path(f1).touch()

#     f2 = next_filename(batch_pattern)
#     assert os.path.basename(f2) == "sd_02_02.png"
#     Path(f2).touch()

#     f3 = next_filename(batch_pattern)
#     assert os.path.basename(f3) == "sd_02_03.png"

#     batch_pattern = next_batch_pattern(pattern, str(tmp_path))
#     assert batch_pattern == os.path.join(tmp_path, "sd_03_##.png")

#     f4 = next_filename(batch_pattern)
#     assert os.path.basename(f4) == "sd_03_01.png"
