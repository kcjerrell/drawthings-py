"""
(Nearly) minimal example of using the Draw Things service.
"""
import asyncio

from drawthings_py import DrawThingsService, Configs, RequestBuilder, FilenamePattern


async def main():
    """
    Generate a single image using the Draw Things service.
    """
    async with DrawThingsService.grpc() as service:
        # Loading a community preset
        # Presets are all guaranteed to work with bridge mode (DT+)
        config = Configs.from_preset("ernie_image_turbo")

        # We can use a filename pattern for incrementing filenames
        # The returned function will always return an unused filename
        next_filename = FilenamePattern("image_###.png", ".")

        # Use the Request Builder to build your image request
        req = RequestBuilder(config, "some random thing", "normal")

        # Pass the request builder to the service
        result = await service.generate_image(req)

        # Results are always a list of ImageBuffers
        result[0].to_file(next_filename())


if __name__ == "__main__":
    asyncio.run(main())