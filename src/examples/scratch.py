import asyncio

from drawthings_py import RequestBuilder, DrawThingsService, ImageBuffer, Config

config = Config.from_json(
    """{"causalInferencePad":0,"preserveOriginalAfterInpaint":true,"seedMode":2,"guidanceScale":1,"shift":3,"strength":1,"sharpness":0,"steps":8,"maskBlurOutset":0,"resolutionDependentShift":false,"width":768,"batchSize":1,"hiresFix":false,"tiledDiffusion":false,"sampler":17,"tiledDecoding":false,"batchCount":1,"loras":[],"model":"z_image_turbo_1.0_q6p.ckpt","height":768,"controls":[],"cfgZeroStar":false,"cfgZeroInitSteps":0,"seed":1012773723,"maskBlur":1.5}"""
)

# if strength is left at 1, this request works
# (the server will ignore the init_image in this case, no matter what it is)
config["strength"] = 0.8


async def main():
    service = DrawThingsService.grpc()

    req = RequestBuilder(
        config,
        "an image of a male superhero, with cybernetic and alien features",
    )
    # without this line, the request works
    req.init_image("scratch_07.png")

    def on_preview(image: ImageBuffer, step: int):
        print(f"Received preview image at step {step}")
        image.to_file(f"prev_{step}.png")

    req.on_preview(on_preview)

    # failure occurs here
    result = await service.generate_image(req)
    result[0].to_file("scratch_07.png")

    service.dispose()


if __name__ == "__main__":
    asyncio.run(main())
