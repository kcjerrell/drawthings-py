import asyncio
from drawthings_py import (
    DrawThingsService,
    Configs,
    RequestBuilder,
    FilenamePattern,
    random_seed,
)


async def main():
    async with DrawThingsService.grpc() as service:
        config = Configs.from_preset("sdxl")
        config["width"] = 768
        config["height"] = 512

        next_filename = FilenamePattern("image_###.png", ".")

        req = RequestBuilder(config, "an ice dragon")

        # we want to use the same seed for the whole batch, so we use get_seed()
        # if we left seed at -1, it would use a different seed for every image
        req.config["seed"] = random_seed()

        req.prompt(
            "an ice dragon, and lots of keywords like awesome, high quality, masterpiece"
        )
        req.negative_prompt("ugly, low quality, fire, cat")

        for i in range(4):
            # we will see how the image looks with various CFGs
            req.config["guidance_scale"] = 2 + 1.4 * i
            result = await service.generate_image(req)

            # save the result, using the same filename pattern for safely incrementing filenames
            result[0].to_file(next_filename())


if __name__ == "__main__":
    asyncio.run(main())
