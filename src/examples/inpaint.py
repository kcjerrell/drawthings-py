"""
Simple example of how to use a mask for inpainting
Can run on DT+ with bridge mode or locally with z_image_turbo_1.0_q6p.ckpt
"""

import asyncio
import numpy as np

from drawthings_py import DrawThings, Configs, RequestBuilder
from drawthings_py.image_buffer import ImageBuffer


def box_mask(width: int, height: int) -> ImageBuffer:
    """
    Create a 1 channel image with left side black and right side white
    """
    img = np.full((height, width), 255, dtype=np.uint8)
    img[0:height, 0 : width // 2] = 0
    return ImageBuffer(img.tobytes(), width, height, 1)


async def main():
    """
    Using a mask for inpainting
    """
    async with DrawThings.grpc() as service:
        # Loading a community preset
        config = Configs.from_preset("z_image_turbo")
        config["width"] = 768
        config["height"] = 768

        # Use the Request Builder to build your image request
        req = RequestBuilder(config, "a beautiful, serene forest")

        # Pass the RequestBuilder to the service. Results are always a list of ImageBuffers
        # Since we are only generating one image, we could write this...
        # result = await service.generate_image(req)
        # result[0].to_file("inpaint_before.png")

        # Or we can get the first (and only) item in the results like this... (note the comma)
        (result,) = await service.generate_image(req)
        result.to_file("inpaint_before.png")

        # Generate a mask and save a preview
        mask = box_mask(768, 768)
        mask.to_file("inpaint_mask.png")

        # We can reuse the same RequestBuilder, and add our image and mask
        req.mask(mask)
        req.init_image("inpaint_before.png")

        # Change some settings and prompt
        req.config["strength"] = 0.97
        req.config["mask_blur"] = 50
        req.prompt("a raging forest fire")

        # Generate!
        result = await service.generate_image(req)
        result[0].to_file("inpaint_result.png")


if __name__ == "__main__":
    asyncio.run(main())
