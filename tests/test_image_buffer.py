from pathlib import Path
import numpy as np
from drawthings_py import ImageBuffer
import struct

def test_image_buffer():
    pixels = bytearray(100 * 100 * 3)
    for x in range(100):
        for y in range(0, 100, 2):
            idx = (y * 100 + x) * 3
            pixels[idx : idx + 3] = [255, 255, 255]
    img_buf = ImageBuffer(pixels, 100, 100, 3)

    assert img_buf.width == 100 and img_buf.height == 100 and img_buf.channels == 3
    assert len(img_buf.data) == 100 * 100 * 3
    assert img_buf.format == "rgb"
    
    save_path = Path("test_01.png")
    img_buf.to_file(save_path)
    assert save_path.exists()


def test_resize():
    save_path = Path("test_01.png")
    assert save_path.exists()
    
    img_buf = ImageBuffer.from_file(save_path)
    assert img_buf.width == 100 and img_buf.height == 100 and img_buf.channels == 3
    assert len(img_buf.data) == 100 * 100 * 3
    assert img_buf.format == "rgb"
    
    resized = img_buf.resized(50, 50)
    
    assert resized.width == 50 and resized.height == 50 and resized.channels == 3
    assert len(resized.data) == 50 * 50 * 3
    assert resized.format == "rgb"
    
    # read a diagonal line across image, assert colors are NOT black or white due to interpolation
    for i in range(50):
        idx = (i * 50 + i) * 3
        r, g, b = resized.data[idx : idx + 3]
        assert not (r == 0 and g == 0 and b == 0)  # not black
        assert not (r == 255 and g == 255 and b == 255)  # not white
        
    # assert original buffer is unchanged (size, format)
    
    assert img_buf.width == 100 and img_buf.height == 100 and img_buf.channels == 3
    assert len(img_buf.data) == 100 * 100 * 3
    assert img_buf.format == "rgb"
    
def test_to_from_tensor():
    # to test conversion to and from tensor format, we will create a small pattern
    # using rgb pixel bytes, and create the equivalent using float16. 
    # then we'll convert each and compare it to the other
    
    pixels = bytearray(48 * 48 * 3)
    tensor = np.zeros((48, 48, 3), dtype=np.float16)
    for x in range(48):
        for y in range(48):
            idx = (y * 48 + x) * 3
            r = 255 if x % 3 == 0 else 0
            g = 255 if x % 3 == 1 else 0
            b = 255 if x % 3 == 2 else 0
            fade = int(255 * (y / 47))  # fade from top to bottom 
            r = min(255, r + fade)
            g = min(255, g + fade)
            b = min(255, b + fade)
            pixels[idx : idx + 3] = [r, g, b]
            
            r, g, b = r / 255.0, g / 255.0, b / 255.0 # 0 - 1
            r, g, b = r * 2 - 1, g * 2 - 1, b * 2 - 1 # -1 to 1
            tensor[y, x, 0] = r
            tensor[y, x, 1] = g
            tensor[y, x, 2] = b


    # the tensor needs to be converted to bytes with a header
    header = bytearray(68)
    struct.pack_into(
        "<9I",
        header,
        0,
        0,
        0x1,  # CCV_TENSOR_CPU_MEMORY,
        0x2,  # CCV_TENSOR_FORMAT_NCHW,
        0x20000,  # CCV_16F,
        0,
        1,
        48,
        48,
        3,
    )
    tensor = header + tensor.tobytes()

    # the img buffer just need to be given its bytes
    img_buf = ImageBuffer(pixels, 48, 48, 3)
  
    tensor_from_buf = img_buf.to_tensor()
    buf_from_tensor = ImageBuffer.from_tensor(tensor)
    # convert the tensor produced from the buffer back into an ImageBuffer
    buf_from_tensor_from_buf = ImageBuffer.from_tensor(tensor_from_buf)

    # basic metadata checks
    assert buf_from_tensor.width == 48 and buf_from_tensor.height == 48 and buf_from_tensor.channels == 3
    assert buf_from_tensor_from_buf.width == 48 and buf_from_tensor_from_buf.height == 48 and buf_from_tensor_from_buf.channels == 3

    # compare pixel data (uint8) allowing +/-1 difference due to float16 quantization
    a = np.frombuffer(buf_from_tensor.data, dtype=np.uint8)
    b = np.frombuffer(buf_from_tensor_from_buf.data, dtype=np.uint8)
    orig = np.frombuffer(img_buf.data, dtype=np.uint8)

    assert a.size == b.size == orig.size

    max_diff_ab = int(np.max(np.abs(a.astype(np.int16) - b.astype(np.int16))))
    max_diff_aorig = int(np.max(np.abs(a.astype(np.int16) - orig.astype(np.int16))))

    assert max_diff_ab <= 1
    assert max_diff_aorig <= 1

    # also ensure overall equality isn't wildly off
    assert np.mean(np.abs(a.astype(np.int16) - orig.astype(np.int16))) <= 0.5
    