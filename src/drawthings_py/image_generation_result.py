from __future__ import annotations

from collections.abc import Sequence
from typing import overload, override

from drawthings_py.image.image_buffer import ImageBuffer


class ImageGenerationResult(Sequence[ImageBuffer]):
    images: list[ImageBuffer]

    def __init__(self, images: list[ImageBuffer]):
        self.images = images

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
            return ImageGenerationResult(self.images[index])
        return self.images[index]
