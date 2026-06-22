from __future__ import annotations

from collections.abc import Sequence
from typing import overload
from typing_extensions import override

from drawthings_py.grpc.audio import AudioBuffer
from drawthings_py.image.image_buffer import ImageBuffer


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
    def __getitem__(self, index: int | slice) -> ImageBuffer | ImageGenerationResult:
        if isinstance(index, slice):
            return ImageGenerationResult(images=self.images[index])
        return self.images[index]
