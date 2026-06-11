"""
ControlNet example
"""

import asyncio

from drawthings_py import DrawThings, Configs, RequestBuilder
from drawthings_py.configs import ControlInputType


async def main():
    """
    Using control images with a controlnet to generate an image
    """
    async with DrawThings.grpc() as service:
        # We'll use two configs in this example, both will work with DT+
        # Flux.2 Klein 4b to create our orignal image
        config_a = Configs.from_preset("flux_2_klein_4b")
        config_a.set(width=768, height=768)

        # And we'll use a Flux.1 model with Union Pro to demonstrate using control nets
        config_b = Configs.from_preset("flux_1_dev")
        config_b.set(
            width=768,
            height=768,
            model="rayflux_v3.0_aio_q5p.ckpt",
            steps=20,
        )

        # Use GenConfig.add_control() to add a ControlNet model to the config
        config_b.add_control(
            file="controlnet_union_pro_flux_1_dev_1.0_q8p.ckpt",
            inputOverride=ControlInputType.Gray,
        )

        # Create a request with our first config
        req_a = RequestBuilder(
            config_a,
            "An image featuring a closeup of a flower. in the background, abstract painted rainbow swirls of color",
        )

        # Gen our source image
        (original,) = await service.generate_image(req_a)
        original.to_file("control_source.png")

        # ImageBuffers can be resized. In this case, we aren't changing size, but we will
        # set the channels to 1 to get a grayscale version
        gray = original.resized(768, 768, channels=1)
        gray.to_file("control_gray.png")

        # Create a request with our second config and add the control image
        req_b = RequestBuilder(
            config_b,
            "A vividly colorful piece of art. A vibrantly yellow flower in front of a purple and blue swirls",
        )
        req_b.control_image(gray, "custom")

        # Generate a recolored version of the image
        (result,) = await service.generate_image(req_b)
        result.to_file("control_final.png")


if __name__ == "__main__":
    asyncio.run(main())
