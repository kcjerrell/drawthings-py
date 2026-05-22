import asyncio

from drawthings_py import RequestBuilder, DrawThingsService, ImageBuffer, Config
import configs

config = configs.klein4


async def main():
    # you can also use DrawThingsService.cli()
    service = DrawThingsService.grpc()

    prev_count = 0

    def on_preview(image: ImageBuffer, step: int):
        nonlocal prev_count
        print(f"Received preview image at step {step}")
        prev_count += 1
        image.to_file(f"previews/prev_{prev_count}.png")

    req = RequestBuilder(
        config,
        "a canny style image of a futuristic superhero, with cybernetic and alien features. white lines on black background",
    )
    req.on_preview(on_preview)
    result = await service.generate_image(req)
    result[0].to_file("scratch_05.png")

    req = RequestBuilder(
        configs.flux_canny, "a futuristic superhero, with cybernetic features"
    )
    req.control_image(result[0], "custom")
    req.on_preview(on_preview)
    result = await service.generate_image(req)
    result[0].to_file("scratch_06.png")

    service.dispose()


if __name__ == "__main__":
    asyncio.run(main())
