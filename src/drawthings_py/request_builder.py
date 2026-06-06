"""
Request builder for constructing Draw Things gRPC image generation requests.
"""
# pyright: reportPrivateUsage=none

from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Literal, TypeAlias, cast
import os
import copy

from .seed_provider import SeedProvider
from .image_buffer import ImageBuffer
from .generated.dt_grpc import image_service
from .configs.types import ConfigDict
from .configs._gen_config import build_config

ImageSource: TypeAlias = str | os.PathLike[str] | ImageBuffer
"""Type alias for image sources, which can be file paths or ImageBuffer instances."""

PromptProcessor: TypeAlias = Callable[[str], str]
"""Type alias for a prompt processing function that takes a string and returns a modified string."""

ProgressCallback: TypeAlias = Callable[
    [image_service.ImageGenerationSignpostProto | None, ImageBuffer | None], None
]

ControlType = Literal[
    "depth",
    "pose",
    "scribble",
    "color",
    "shuffle",
    "custom",
]
"""Supported control image types."""

control_types = [
    "depth",
    "pose",
    "scribble",
    "color",
    "shuffle",
    "custom",
]


class _Unchanged:
    pass


_UNCHANGED = _Unchanged()


@dataclass
class ControlImage:
    """Represents a control image with a type and weight.

    Attributes:
        image: The image buffer containing the control image data.
        type: The type of control image  (e.g., depth, pose).
        weight: The strength/influence weight of the control image.
    """

    image: ImageBuffer
    type: ControlType
    weight: float


class RequestBuilder:
    """A builder class for constructing image generation requests

    Attributes:
        config: The image generation configuration dictionary.
    """

    config: ConfigDict
    _seed_provider: SeedProvider

    _prompt: str | None
    _negative_prompt: str | None
    _init_image: ImageBuffer | None
    _mask: ImageBuffer | None
    _mask_threshold: int | None = 127
    _mask_use_alpha: bool = False
    _control_images: dict[ControlType, ControlImage]
    _moodboard: list[ControlImage]

    _process_prompt: PromptProcessor | None
    _on_progress: ProgressCallback | None

    def __init__(
        self,
        config: ConfigDict,
        prompt: str | None = None,
        negative_prompt: str | None = None,
    ):
        """Initializes the RequestBuilder with configuration and optional prompts.

        Args:
            config: A dictionary containing the image generation settings (e.g. width, height).
            prompt: The main text prompt for generation.
            negative_prompt: The negative text prompt for generation.
        """
        self.config = copy.deepcopy(config)
        self._seed_provider = SeedProvider()

        self._init_image = None
        self._mask = None
        self._control_images = {}
        self._moodboard = []
        self._prompt = prompt
        self._negative_prompt = negative_prompt

        self._process_prompt = None
        self._on_progress = None

    def prompt(
        self, prompt: str | None, negative_prompt: str | None | _Unchanged = _UNCHANGED
    ):
        """Sets the positive and/or negative text prompts.

        Args:
            prompt: The main text prompt.
            negative_prompt: The negative text prompt. Use None to clear.
        """
        self._prompt = prompt
        if negative_prompt is not _UNCHANGED:
            self._negative_prompt = cast(str | None, negative_prompt)

    def negative_prompt(self, negative_prompt: str | None = None):
        """Sets the negative text prompt.

        Args:
            negative_prompt: The negative text prompt.
        """
        self._negative_prompt = negative_prompt

    def seed_seed(self, x: str | bytes | float | int | None):
        """
        Re-initialize the seed provider.
        """
        self._seed_provider = SeedProvider(x)

    def control_image(
        self,
        image: ImageSource,
        control_type: ControlType,
        weight: float = 1.0,
    ):
        """Sets the control image with an optional weight.

        Args:
            image: The path to the image file or an ImageBuffer instance.
            control_type: The type of control (e.g., "depth", "pose").
            weight: The strength/influence weight of the control image (default: 1.0).
        """
        self._control_images[control_type] = ControlImage(
            _get_image_from_arg(image), control_type, weight
        )

    def clear_control_image(
        self,
        control_type: ControlType,
    ):
        """Removes the control image of the specified type.

        Args:
            control_type: The type of control image to remove.
        """
        if control_type in self._control_images:
            del self._control_images[control_type]

    def add_moodboard_image(self, image: ImageSource, weight: float = 1.0):
        """Adds a moodboard image for shuffle/style guidance.

        Args:
            image: The path to the image file or an ImageBuffer instance.
            weight: The weight of the moodboard image (default: 1.0).
        """
        hint = ControlImage(_get_image_from_arg(image), "shuffle", weight)
        self._moodboard.append(hint)

    def set_moodboard_images(
        self, images: list[ImageSource], weights: list[float] | None = None
    ):
        """Sets the collection of moodboard images, clearing any existing ones.

        Args:
            images: A list of image paths or ImageBuffer instances.
            weights: Optional list of weights corresponding to the images.
                If fewer weights are provided than images, remaining weights default to 1.0.
        """
        self._moodboard.clear()
        for index, image in enumerate(images):
            weight = (
                weights[index] if weights is not None and index < len(weights) else 1.0
            )
            self.add_moodboard_image(image, weight)

    def clear_moodboard(self):
        """Clears all moodboard images."""
        self._moodboard.clear()

    def init_image(self, image: ImageSource):
        """
        Sets the initial image for image-to-image generation. Note: alpha channel will be ignored.
        If you want to use the alpha channel as a mask, use .mask(image, use_alpha=True)

        Args:
            image: The path to the image file or an ImageBuffer instance.
        """
        self._init_image = _get_image_from_arg(image)

    def clear_init_image(self):
        """Clears the initial image."""
        self._init_image = None

    def mask(
        self, mask: ImageSource, use_alpha: bool = False, threshold: int | None = 127
    ):
        """Sets the mask image for inpainting generation. Draw Things uses a binary mask,
        meaning white pixels are inpainted and black pixels are preserved. If your mask image has
        3 channels, it will be converted to grayscale. Then all pixels below a threshold (default=127,
        approximately 50% lightness) will be considered masked (preserved).

        If your mask image has an alpha channel, it will be ignored unless you set use_alpha=True

        Args:
            mask: The path to the mask image file or an ImageBuffer instance.
            use_alpha: If True, use the alpha channel as the mask instead of converting to grayscale. if the image doesn't have an alpha channel, this parameter is ignored.
            threshold: The threshold value for converting the mask to binary (0-255). Pixels below this value will be masked.
        """
        self._mask = _get_image_from_arg(mask)
        self._mask_use_alpha = use_alpha
        self._mask_threshold = threshold

    def clear_mask(self):
        """Clears the mask image."""
        self._mask = None
        self._mask_use_alpha = False
        self._mask_threshold = 127

    def on_progress(self, callback: ProgressCallback | None):
        """Registers a callback function to handle generation preview updates.
        Note: this API is likely to change. Also, preview images may be discolored

        Args:
            callback: A callable to receive progress updates. It should accept two arguments: a dictionary containing signpost information, and an ImageBuffer of the preview image.
        """
        self._on_progress = callback

    def prompt_processor(self, fn: PromptProcessor | None):
        """Registers a function to process the prompt before a request is sent.
        Note: This API is likely to change

        Args:
            callback: A callable that takes the original prompt string and returns a modified version.
        """
        self._process_prompt = fn

    def update_config(self, config: ConfigDict):
        """Updates the configuration for this request.

        Args:
            config: A dictionary containing configuration parameters.
        """
        self.config.update(config)

    def _active_hint(self) -> list[tuple[ControlType, list[ControlImage]]]:
        """Collects and returns active control images and moodboard hints.

        Returns:
            list[tuple]: A list of tuples pairing HintType with a list of active Hint objects.
        """
        active_hint_types: list[tuple[ControlType, list[ControlImage]]] = [
            (k, [v]) for k, v in self._control_images.items()
        ]
        if len(self._moodboard) > 0:
            active_hint_types.extend([("shuffle", [v for v in self._moodboard])])
        return active_hint_types


def _get_image_from_arg(arg: str | os.PathLike[str] | ImageBuffer) -> ImageBuffer:
    """Helper to resolve different image argument types into an ImageBuffer.

    Args:
        arg: A file path (str or PathLike) or an existing ImageBuffer.

    Returns:
        ImageBuffer: The resolved image buffer instance.

    Raises:
        TypeError: If the argument type is not supported.
    """
    if isinstance(arg, ImageBuffer):
        return arg
    return ImageBuffer.from_file(arg)


def _get_hint_channels(hint_type: ControlType) -> int | None:
    """Determines the expected number of channels for a given hint type.

    Args:
        hint_type: The category of hint (e.g. depth, pose).

    Returns:
        int or None: 1 for depth/scribble hints; None for other types.
    """
    if hint_type == "depth" or hint_type == "scribble":
        return 1
    else:
        return None


def build_grpc_message(
    builder: RequestBuilder,
) -> tuple[image_service.ImageGenerationRequest, ProgressCallback | None]:
    """Builds the gRPC ImageGenerationRequest message.

    Constructs and configures the request object with settings from `config`,
    as well as prompt, initial images, masks, and hints.

    (Note: the DrawThings service will call this automaticlly)

    Returns:
        tuple: A tuple containing:
            - ImageGenerationRequest: The fully configured gRPC request message.
            - callable or None: The registered preview callback, if any.
    """
    # pylint: disable=protected-access

    message = image_service.ImageGenerationRequest()

    # configuration
    # check for seed
    config_seed = builder.config.get("seed", -1)
    req_seed = (
        config_seed if config_seed > 0 else builder._seed_provider.get_seed(config_seed)
    )

    message.configuration = build_config(builder.config, req_seed)

    width = builder.config.get("width") or 512
    height = builder.config.get("height") or 512

    # image
    if builder._init_image:
        resized = builder._init_image.resized(width, height, 3)
        message.image = resized.to_tensor()

    # mask
    if builder._mask:
        resized = builder._mask.resized(width, height)
        message.mask = resized.to_binary_mask(
            builder._mask_use_alpha, builder._mask_threshold
        )

    # hints
    for hint_type, hints in builder._active_hint():
        if len(hints) == 0:
            continue

        tensors: list[image_service.TensorAndWeight] = []
        for hint in hints:
            hint_image = hint.image
            if hint_type != "shuffle":
                hint_image = hint.image.resized(
                    width,
                    height,
                    _get_hint_channels(hint_type),
                )
            tensor = hint_image.to_tensor()
            tensors.append(
                image_service.TensorAndWeight(tensor=tensor, weight=hint.weight)
            )

        message.hints.append(
            image_service.HintProto(
                hint_type=hint_type,
                tensors=tensors,
            )
        )

    # prompt
    prompt = builder._prompt or ""
    if builder._process_prompt is not None:
        prompt = builder._process_prompt(prompt)
    message.prompt = prompt

    # negativePrompt
    message.negative_prompt = builder._negative_prompt or ""

    # scaleFactor
    message.scale_factor = 1

    # override
    # keywords - unused
    # user
    message.user = os.getlogin()
    # device
    # contents - will not use, prefer image and hints directly
    # sharedSecret
    # chunked - leave default

    return message, builder._on_progress


def build_command(
    builder: RequestBuilder,  # pyright: ignore[reportUnusedParameter]
) -> list[str]:
    """Builds the CLI command representing the generation options.

    Note: This is currently a stub implementation.

    Returns:
        list[str]: The command-line arguments list.
    """
    return []
