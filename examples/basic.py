"""
Minimal example of using the Draw Things service.
"""

import asyncio

from drawthings_py import DrawThings, Configs, RequestBuilder


async def main():
    """
    Generate a single image using the Draw Things service.
    """
    async with DrawThings.grpc() as service:
        # Loading a community preset
        # Presets are all guaranteed to work with bridge mode (DT+)
        config = Configs.from_preset("z_image_turbo")

        # Use the Request Builder to build your image request
        req = RequestBuilder(
            config,
            "An astronaut in a space helmet riding a bucking bronco on an alien planet",
        )

        # Pass the request builder to the service
        # Results are always a list of ImageBuffers. Since we are only generating one image,
        # you can unpack the result to get the first (and only) ImageBuffer
        # (Note the parenthesis and comma)
        (result,) = await service.generate(req)

        result.to_file("astrorider.png")


if __name__ == "__main__":
    asyncio.run(main())
