from __future__ import annotations

import importlib.util
from collections.abc import Sequence
from typing import overload
from typing_extensions import override
import tempfile

import numpy as np

from drawthings_py.grpc.audio import AudioBuffer
from drawthings_py.image.image_buffer import ImageBuffer
from drawthings_py.util._errors import InvalidDrawThingsResponseError

_IMAGEIO_AVAILABLE = importlib.util.find_spec("imageio_ffmpeg") is not None  # type: ignore[import-not-found]


class ImageGenerationResult(Sequence[ImageBuffer]):
    """
    Contains the result of an image generation request.
    """

    images: list[ImageBuffer]
    """Contains all generated images/frames"""
    audio: AudioBuffer | None
    """Contains the generated audio, if any"""

    def __init__(self, *, images: list[ImageBuffer], audio: AudioBuffer | None = None):
        self.images = images
        self.audio = audio

    @override
    def __len__(self) -> int:
        return len(self.images)

    @overload
    def __getitem__(self, index: int) -> ImageBuffer: ...
    @overload
    def __getitem__(self, index: slice) -> ImageGenerationResult: ...
    @override
    def __getitem__(
        self, index: int | slice[int, int, int]
    ) -> ImageBuffer | ImageGenerationResult:
        if isinstance(index, slice):
            audio: AudioBuffer | None = None
            start, stop, step = index.indices(len(self))
            if self.audio is not None and step == 1:
                audio = self.get_audio_segment(start, stop)
            return ImageGenerationResult(images=self.images[index], audio=audio)
        return self.images[index]

    def get_audio_segment(self, start_frame: int, end_frame: int) -> AudioBuffer | None:
        """
        Extracts an audio segment from the audio buffer based on video frame indices. This
        is used internally when slicing the ImageGenerationResult so that the audio matches
        the sliced frames. Returns None if there is no audio.

        Args:
            start_frame: The starting frame index (inclusive).
            end_frame: The ending frame index (exclusive).

        Returns:
            An AudioBuffer containing the audio segment, or None if no audio is available.

        Raises:
            ValueError: If the frame indices are out of bounds or invalid.
        """
        if self.audio is None:
            return None
        if start_frame < 0 or end_frame > len(self):
            raise ValueError("Audio segment out of bounds")
        if start_frame >= end_frame:
            raise ValueError("Start frame must be less than end frame")
        start_pos = start_frame / len(self)
        end_pos = end_frame / len(self)
        return self.audio.slice(start_pos, end_pos)

    def to_video(
        self, path: str, fps: int = 24, codec: str = "libx264", quality: int = 8
    ) -> None:
        """Converts the images in this result to a video file.

        Args:
            path: Output file path for the video (e.g., "output.mp4").
            fps: Frames per second for the video. Defaults to 24.
            codec: Video codec to use. Defaults to "libx264".
            quality: Quality parameter for the codec (0-10 for libx264). Defaults to 8.

        Raises:
            ImportError: If imageio is not installed. Install with `pip install drawthings-py[ffmpeg]`.
            ValueError: If there are no images to convert.
        """
        if not _IMAGEIO_AVAILABLE:
            raise ImportError(
                "imageio_ffmpeg is required for video export. "
                "Install it with: pip install drawthings-py[ffmpeg]"
            )

        if not self.images:
            raise ValueError("No images to convert to video")

        from imageio_ffmpeg import write_frames

        _check_frame_consistency(self.images)

        width = self.images[0].width
        height = self.images[0].height

        audio_path: str | None = None
        vid = None

        with tempfile.NamedTemporaryFile(suffix=".wav") as tmp_audio:
            try:
                if self.audio:
                    self.audio.to_file(tmp_audio.name)
                    audio_path = tmp_audio.name

                frames = (_to_frame(img) for img in self.images)

                # Write video using imageio
                vid = write_frames(
                    path=path,
                    size=(width, height),
                    fps=fps,
                    quality=quality,
                    codec=codec,
                    audio_path=audio_path,
                )
                _ = vid.send(None)
                for frame in frames:
                    _ = vid.send(frame)
                vid.close()

            except Exception as e:
                if vid is not None:
                    vid.close()
                raise e


# Convert ImageBuffer objects to numpy arrays
def _to_frame(img: ImageBuffer) -> bytes:
    arr = np.frombuffer(img.data, dtype=np.uint8).reshape(
        img.height, img.width, img.channels
    )
    return arr.tobytes()


def _check_frame_consistency(frames: list[ImageBuffer]):
    if len(frames) == 0:
        raise InvalidDrawThingsResponseError("The Draw Things API returned no images")

    width = frames[0].width
    height = frames[0].height
    channels = frames[0].channels

    if channels != 3 and channels != 4:
        raise InvalidDrawThingsResponseError(
            "The Draw Things API returned images with an unsupported number of channels"
        )

    for frame in frames:
        if frame.width != width or frame.height != height or frame.channels != channels:
            raise InvalidDrawThingsResponseError(
                "The Draw Things API returned images of different sizes"
            )
