import math
import os
import struct
from dataclasses import dataclass
from typing import Any, Literal, cast

import fpzip
import numpy as np
from PIL import Image

from ._png_writer import write_png_with_usercomment

_TENSOR_HEADER_SIZE = 68
_FPZIP_MAGIC = 1012247


def _c134(channels: int) -> Literal[1, 3, 4]:
    if channels not in (1, 3, 4):
        raise ValueError(f"Invalid number of channels: {channels}")
    return cast(Literal[1, 3, 4], channels)


@dataclass(frozen=True)
class ImageBuffer:
    """A container for an image buffer with raw pixel bytes.

    This class encapsulates the raw bytes of an image along with its dimensions and
    color channels, providing utility methods for resizing, file I/O, and converting
    to and from Draw Thing's tensor format

    Attributes:
        data: Raw byte array representing the pixel values.
        width: Width of the image in pixels.
        height: Height of the image in pixels.
        channels: Number of color channels (1 for grayscale, 3 for RGB, 4 for RGBA).
    """

    data: bytes
    width: int
    height: int
    channels: Literal[1, 3, 4]
    metadata: dict[str, Any] | None = None

    @property
    def format(self) -> str:
        """Returns the string representation of the color format.

        Returns:
            str: One of "gray", "rgb", or "rgba".
        """
        return {
            1: "gray",
            3: "rgb",
            4: "rgba",
        }[self.channels]

    @property
    def prompt(self) -> str | None:
        return self.metadata.get("c") if self.metadata is not None else None

    @property
    def negative_prompt(self) -> str | None:
        return self.metadata.get("uc") if self.metadata is not None else None

    def __post_init__(self):
        """Validates that the provided byte buffer size matches the image dimensions.

        Raises:
            ValueError: If the length of `data` does not equal `width * height * channels`.
        """
        expected = self.width * self.height * self.channels
        actual = len(self.data)

        if actual != expected:
            raise ValueError(
                f"ImageBuffer size mismatch: "
                f"{self.width}x{self.height}x{self.channels} = {expected} bytes, "
                f"but got {actual} bytes"
            )

    @classmethod
    def from_tensor(
        cls, tensor: bytes, metadata: dict[str, Any] | None = None
    ) -> "ImageBuffer":
        """Deserializes and decodes an ImageBuffer from a CCV tensor byte stream.

        This method reads a 68-byte CCV tensor header, extracts the image metadata
        (width, height, channels), handles compression (fpzip), de-quantizes the
        float16 data from [-1.0, 1.0] back to uint8 pixel values [0, 255], and validates
        integrity.

        Args:
            tensor: The raw byte sequence of the serialized CCV tensor.

        Returns:
            ImageBuffer: The decoded image buffer containing uint8 pixels.

        Raises:
            ValueError: If the tensor header or payload is truncated, if dimensions/channels
                are invalid, or if the payload contains NaN values.
        """
        if len(tensor) < _TENSOR_HEADER_SIZE:
            raise ValueError(
                f"Tensor buffer must include a {_TENSOR_HEADER_SIZE}-byte header"
            )

        int_buffer = np.frombuffer(tensor, dtype="<u4", count=17)
        height, width, channels = map(int, int_buffer[6:9])

        if width <= 0 or height <= 0:
            raise ValueError(f"Invalid tensor dimensions: {width}x{height}")
        if channels not in (1, 3, 4):
            raise ValueError(f"Unsupported tensor channel count: {channels}")

        expected_values = width * height * channels
        if int(int_buffer[0]) == _FPZIP_MAGIC:
            decompressed = fpzip.decompress(tensor[_TENSOR_HEADER_SIZE:], order="C")
            fp16_data = np.asarray(decompressed, dtype=np.float16).reshape(-1)
            fp16_data = fp16_data[:expected_values]
        else:
            expected_bytes = _TENSOR_HEADER_SIZE + (expected_values * 2)
            if len(tensor) < expected_bytes:
                raise ValueError(
                    f"Tensor payload is too short: expected {expected_bytes} bytes, "
                    f"got {len(tensor)} bytes"
                )
            fp16_data = np.frombuffer(
                tensor,
                dtype="<f2",
                count=expected_values,
                offset=_TENSOR_HEADER_SIZE,
            )

        if fp16_data.size != expected_values:
            raise ValueError(
                f"Tensor payload size mismatch: expected {expected_values} values, "
                f"got {fp16_data.size}"
            )
        if np.isnan(fp16_data).any():
            raise ValueError("Tensor payload contains NaN values")

        # De-quantize float16 values from [-1, 1] to [0, 255] uint8 pixels.
        data = np.clip(np.round((fp16_data + 1) * 127.5), 0, 255).astype(np.uint8)
        return cls(
            data=data.tobytes(),
            width=width,
            height=height,
            channels=_c134(channels),
            metadata=metadata,
        )

    def to_file(self, path: str | os.PathLike[str]) -> None:
        """Saves the image buffer contents to a file.

        Args:
            path: Target file path or PathLike object where the image should be written.
        """
        mode = {
            1: "L",
            3: "RGB",
            4: "RGBA",
        }[self.channels]

        if str(path).lower().endswith(".png") and self.metadata is not None:
            png_bytes = write_png_with_usercomment(
                self.data, self.width, self.height, self.channels, self.metadata
            )
            with open(path, "wb") as f:
                f.write(png_bytes)
        else:
            Image.frombytes(mode, (self.width, self.height), self.data).save(path)

    @classmethod
    def from_file(cls, path: str | os.PathLike[str]) -> "ImageBuffer":
        """Loads and decodes an image file into an ImageBuffer.

        Args:
            path: Source file path or PathLike object of the image to load.

        Returns:
            ImageBuffer: An image buffer containing the decoded pixel bytes.
        """
        img = Image.open(path)
        channels = len(img.getbands())

        return cls(
            data=img.tobytes(),
            width=img.width,
            height=img.height,
            channels=_c134(channels),
        )

    def resized(
        self, width: int, height: int, channels: int | None = None
    ) -> "ImageBuffer":
        """Resizes the image buffer and/or converts its color format.

        Uses bilinear interpolation for the resizing operation. If the requested
        dimensions and channels match the current state, `self` is returned directly.

        Args:
            width: Target width in pixels.
            height: Target height in pixels.
            channels: Target channel count (1, 3, or 4). Defaults to current channel count.

        Returns:
            ImageBuffer: A new ImageBuffer instance with the requested configuration.
        """
        output_channels = channels if channels is not None else self.channels
        output_channels = _c134(output_channels)

        if (
            width == self.width
            and height == self.height
            and output_channels == self.channels
        ):
            return self

        arr = np.frombuffer(self.data, dtype=np.uint8).reshape(
            self.height, self.width, self.channels
        )

        if self.channels == 1:
            arr = arr.squeeze()

        img = Image.fromarray(arr, get_format(self.channels))

        if output_channels != self.channels:
            img = img.convert(get_format(output_channels))

        img = img.resize((width, height), Image.Resampling.BILINEAR)

        return ImageBuffer(
            data=img.tobytes(),
            width=img.width,
            height=img.height,
            channels=_c134(output_channels),
        )

    def cropped(
        self,
        *,
        left: int = 0,
        top: int = 0,
        right: int = 0,
        bottom: int = 0,
        fill: int = 0,
    ) -> "ImageBuffer":
        """Crops the image to the given dimensions.

        Args:
            left: Left edge of the crop region.
            top: Top edge of the crop region.
            right: Right edge of the crop region.
            bottom: Bottom edge of the crop region.

        Returns:
            ImageBuffer: A new ImageBuffer instance with the requested configuration.
        """
        x0, y0 = left, top
        x1, y1 = self.width - right, self.height - bottom

        out_w = x1 - x0
        out_h = y1 - y0

        if out_w <= 0 or out_h <= 0:
            raise ValueError("Final dimensions must be greater than 0")

        arr = np.frombuffer(self.data, dtype=np.uint8).reshape(
            self.height, self.width, self.channels
        )

        h, w = arr.shape[:2]
        c = arr.shape[2] if arr.ndim == 3 else 1

        out = np.full(
            (out_h, out_w, c) if c > 1 else (out_h, out_w), fill, dtype=arr.dtype
        )

        # overlap in source space
        src_x0 = max(0, x0)
        src_y0 = max(0, y0)
        src_x1 = min(w, x1)
        src_y1 = min(h, y1)

        if src_x1 <= src_x0 or src_y1 <= src_y0:
            return ImageBuffer(out.tobytes(), out_w, out_h, self.channels)

        # map to destination space
        dst_x0 = src_x0 - x0
        dst_y0 = src_y0 - y0

        dst_x1 = dst_x0 + (src_x1 - src_x0)
        dst_y1 = dst_y0 + (src_y1 - src_y0)

        out[dst_y0:dst_y1, dst_x0:dst_x1] = arr[src_y0:src_y1, src_x0:src_x1]

        return ImageBuffer(out.tobytes(), out_w, out_h, self.channels)

    def center_cropped(
        self, width: int, height: int, channels: int | None = None
    ) -> "ImageBuffer":
        """Resizes the image to the given dimensions, preserving aspect ratio via center crop.

        Scales the image so that both target dimensions are fully covered (scale-to-fill),
        then center-crops the result to the exact requested size. If the requested
        dimensions and channels already match, ``self`` is returned directly.

        Args:
            width: Target width in pixels.
            height: Target height in pixels.
            channels: Target channel count (1, 3, or 4). Defaults to current channel count.

        Returns:
            ImageBuffer: A new ImageBuffer cropped to exactly ``width × height``.
        """
        current_ar = self.width / self.height  # 1024x1024 , 1.0
        target_ar = width / height  # 512x768, 0.666

        cropped = self

        if current_ar > target_ar:
            # the image is wider than requested, so crop the sides evenly
            crop_width = width / target_ar
            excess = self.width - crop_width
            cropped = self.cropped(
                left=math.ceil(excess / 2), right=math.floor(excess / 2)
            )
        elif current_ar < target_ar:
            # the image is taller than requested so crop the top and bottom evenly
            crop_height = height / target_ar
            excess = self.height - crop_height
            cropped = self.cropped(
                top=math.ceil(excess / 2), bottom=math.floor(excess / 2)
            )

        return cropped.resized(width, height, channels)

    def to_tensor(self) -> bytes:
        """Converts the image buffer into Draw Thing's tensor format

        Converts the uint8 pixel values [0, 255] to float16 within the [-1.0, 1.0] range
        and prepends a 68-byte CCV CPU memory tensor header.

        Returns:
            bytes: The complete serialized tensor byte stream.
        """
        # --- Load into numpy (H, W, C) ---
        arr = np.frombuffer(self.data, dtype=np.uint8).reshape(
            self.height, self.width, self.channels
        )

        # --- Convert to float16 in [-1, 1] ---
        arr = (arr.astype("<f2") / 255.0).astype("<f2")  # [0,1]
        arr = (arr * 2.0 - 1.0).astype("<f2")  # [-1,1]

        header = build_image_header(self.width, self.height, self.channels)

        return header + arr.tobytes()

    def to_binary_mask(self, use_alpha=False, threshold=127) -> bytes:
        """Converts the image buffer into a binary mask tensor.

        If use_alpha is True, the alpha channel is used as the mask. Otherwise, the image is converted to grayscale
        and then thresholded to create a binary mask.

        Args:
            use_alpha: If True, use the alpha channel as the mask. Otherwise, convert to grayscale and threshold.
            threshold: The threshold value for converting the mask to binary (0-255). Pixels below this value will be masked.

        Returns:
            bytes: The complete serialized tensor byte stream.
        """
        # --- Load into numpy (H, W, C) ---
        arr = np.frombuffer(self.data, dtype=np.uint8).reshape(
            self.height, self.width, self.channels
        )

        # --- Convert to grayscale if needed ---
        if use_alpha and self.channels >= 4:
            # Use alpha channel directly
            mask = arr[:, :, 3]
        else:
            # Convert to grayscale
            if self.channels == 3:
                # Convert RGB to grayscale using standard luminance weights
                mask = np.dot(arr[:, :, :3], [0.2989, 0.5870, 0.1140])
            elif self.channels == 1:
                mask = arr[:, :, 0]
            else:
                raise ValueError(f"Unsupported channel count: {self.channels}")

        # --- Threshold to binary ---
        mask = (mask > threshold).astype(np.uint8) * 2

        header = build_image_header(self.width, self.height, 1, is_mask=True)

        return header + mask.tobytes()


def build_image_header(width: int, height: int, channels: int, is_mask=False) -> bytes:
    """Builds a standard 68-byte CCV CPU NCHW tensor header.

    Args:
        width: Width of the image.
        height: Height of the image.
        channels: Channel count.

    Returns:
        bytes: A 68-byte header packed according to the CCV tensor layout.
    """
    header = bytearray(68)

    if is_mask:
        struct.pack_into(
            "<9I",
            header,
            0,
            0,
            0x1,  # CCV_TENSOR_CPU_MEMORY,
            0x2,  # CCV_TENSOR_FORMAT_NCHW,
            0x01000,  # CCV_8U,
            0,
            height,
            width,
            0,
            0,
        )

    else:
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
            height,
            width,
            channels,
        )

    return bytes(header)


def get_format(channels: int) -> str:
    """Maps a channel count to the corresponding PIL mode string.

    Args:
        channels: Channel count (1, 3, or 4).

    Returns:
        str: PIL mode string ('L' for grayscale, 'RGB' for 3 channels, 'RGBA' for 4 channels).

    Raises:
        ValueError: If the channel count is not 1, 3, or 4.
    """
    if channels == 1:
        return "L"
    if channels == 3:
        return "RGB"
    if channels == 4:
        return "RGBA"

    raise ValueError(f"Unsupported channel count: {channels}")
