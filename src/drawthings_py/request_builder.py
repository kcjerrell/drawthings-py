"""
Request builder for constructing Draw Things gRPC image generation requests.
"""

from dataclasses import dataclass
from typing import Callable, Literal, Sequence, TypeAlias
import os
import copy
from .image_buffer import ImageBuffer
from .generated.dt_grpc import image_service
from ._gen_config import build_configuration
from .configs.types import ConfigDict

ImageSource: TypeAlias = str | os.PathLike[str] | ImageBuffer
"""Type alias for image sources, which can be file paths or ImageBuffer instances."""

PromptProcessor: TypeAlias = Callable[[str], str]
"""Type alias for a prompt processing function that takes a string and returns a modified string."""

ProgressCallback: TypeAlias = Callable[[image_service.ImageGenerationSignpostProto | None, ImageBuffer | None], None]

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

    _prompt: str | None
    _negative_prompt: str | None
    _init_image: ImageBuffer | None
    _mask: ImageBuffer | None
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
        self._init_image = None
        self._mask = None
        self._control_images = {}
        self._moodboard = []
        self._prompt = prompt
        self._negative_prompt = negative_prompt

        self._process_prompt = None
        self._on_progress = None

    def prompt(self, prompt: str | None = None, negative_prompt: str | None = None):
        """Sets the positive and/or negative text prompts.

        Args:
            prompt: The main text prompt.
            negative_prompt: The negative text prompt.

        Returns:
            RequestBuilder: The builder instance for chaining.
        """
        self._prompt = prompt
        self._negative_prompt = negative_prompt
        return self

    def negative_prompt(self, negative_prompt: str | None = None):
        """Sets the negative text prompt.

        Args:
            negative_prompt: The negative text prompt.

        Returns:
            RequestBuilder: The builder instance for chaining.
        """
        self._negative_prompt = negative_prompt
        return self

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

        Returns:
            RequestBuilder: The builder instance for chaining.
        """
        self._control_images[control_type] = ControlImage(
            _get_image_from_arg(image), control_type, weight
        )
        return self

    def remove_control_image(
        self,
        control_type: ControlType,
    ):
        """Removes the control image of the specified type.

        Args:
            control_type: The type of control image to remove.

        Returns:
            RequestBuilder: The builder instance for chaining.
        """
        if control_type in self._control_images:
            del self._control_images[control_type]
        return self

    def add_moodboard_image(self, image: ImageSource, weight: float = 1.0):
        """Adds a moodboard image for shuffle/style guidance.

        Args:
            image: The path to the image file or an ImageBuffer instance.
            weight: The weight of the moodboard image (default: 1.0).

        Returns:
            RequestBuilder: The builder instance for chaining.
        """
        hint = ControlImage(_get_image_from_arg(image), "shuffle", weight)
        self._moodboard.append(hint)
        return self

    def set_moodboard_images(
        self, images: list[ImageSource], weights: list[float] | None = None
    ):
        """Sets the collection of moodboard images, clearing any existing ones.

        Args:
            images: A list of image paths or ImageBuffer instances.
            weights: Optional list of weights corresponding to the images.
                If fewer weights are provided than images, remaining weights default to 1.0.

        Returns:
            RequestBuilder: The builder instance for chaining.
        """
        self._moodboard.clear()
        for index, image in enumerate(images):
            weight = (
                weights[index] if weights is not None and index < len(weights) else 1.0
            )
            self.add_moodboard_image(image, weight)
        return self

    def clear_moodboard(self):
        """Clears all moodboard images.

        Returns:
            RequestBuilder: The builder instance for chaining.
        """
        self._moodboard.clear()
        return self

    def init_image(self, image: ImageSource):
        """Sets the initial image for image-to-image generation.

        Args:
            image: The path to the image file or an ImageBuffer instance.

        Returns:
            RequestBuilder: The builder instance for chaining.
        """
        self._init_image = _get_image_from_arg(image)
        return self

    def clear_init_image(self):
        """Clears the initial image.

        Returns:
            RequestBuilder: The builder instance for chaining.
        """
        self._init_image = None
        return self

    def mask(self, mask: ImageSource):
        """Sets the mask image for inpainting generation.

        Args:
            mask: The path to the mask image file or an ImageBuffer instance.

        Returns:
            RequestBuilder: The builder instance for chaining.
        """
        self._mask = _get_image_from_arg(mask)
        return self

    def clear_mask(self):
        """Clears the mask image.

        Returns:
            RequestBuilder: The builder instance for chaining.
        """
        self._mask = None
        return self

    def on_progress(self, callback: ProgressCallback | None):
        """Registers a callback function to handle generation preview updates.
        Note: this API is likely to change. Also, preview images may be discolored

        Args:
            callback: A callable to receive progress updates. It should accept two arguments: a dictionary containing signpost information, and an ImageBuffer of the preview image.

        Returns:
            RequestBuilder: The builder instance for chaining.
        """
        self._on_progress = callback
        return self

    def prompt_processor(self, fn: PromptProcessor | None):
        """Registers a callback function to preprocess the prompt before sending.
        Note: This API is likely to change

        Args:
            callback: A callable that takes the original prompt string and returns a modified version.

        Returns:
            RequestBuilder: The builder instance for chaining.
        """
        self._process_prompt = fn
        return self

    def _active_hint(self) -> list[tuple[ControlType, list[ControlImage]]]:
        """Collects and returns active control images and moodboard hints.

        Returns:
            list[tuple]: A list of tuples pairing HintType with a list of active Hint objects.
        """
        active_hint_types: list[tuple[ControlType, list[ControlImage]]] = [
            (k, [v]) for k, v in self._control_images.items() if v is not None
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
    elif isinstance(arg, str | os.PathLike):
        return ImageBuffer.from_file(arg)
    raise TypeError(f"Unsupported type for image: {type(arg)}")


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


def _build_message(
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
    message.configuration = build_configuration(builder.config)

    width = builder.config.get("width") or 512
    height = builder.config.get("height") or 512

    # image
    if builder._init_image:
        resized = builder._init_image.resized(width, height, 3)
        message.image = resized.to_tensor()

    # mask

    # hints
    for hint_type, hints in builder._active_hint():
        if len(hints) == 0:
            continue

        tensors = []
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


def _build_command(
    builder: RequestBuilder,  # pylint: disable=unused-argument
) -> list[str]:
    """Builds the CLI command representing the generation options.

    Note: This is currently a stub implementation.

    Returns:
        list[str]: The command-line arguments list.
    """
    return []
