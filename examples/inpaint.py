"""
Simple example of how to use a mask for inpainting
Can run on DT+ with bridge mode or locally with z_image_turbo_1.0_q6p.ckpt
"""

import asyncio
import numpy as np

from drawthings_py import DrawThings, Configs, RequestBuilder, ImageBuffer


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
        # config = Configs.from_json(
        #     """{"preserveOriginalAfterInpaint":true,"height":1024,"seed":2462803018,"sampler":1,"negativeOriginalImageHeight":512,"width":1024,"targetImageHeight":1024,"shift":1,"clipSkip":1,"sharpness":3,"negativeAestheticScore":2.5,"maskBlurOutset":0,"upscaler":"","causalInferencePad":0,"strength":1,"negativeOriginalImageWidth":512,"originalImageHeight":1024,"aestheticScore":6,"cropLeft":0,"originalImageWidth":1024,"hiresFix":false,"controls":[],"faceRestoration":"","cropTop":0,"maskBlur":1.5,"zeroNegativePrompt":false,"cfgZeroInitSteps":0,"loras":[],"tiledDecoding":false,"model":"foxaiponyfantastic_v2_f16.ckpt","steps":20,"tiledDiffusion":false,"refinerModel":"","batchSize":1,"guidanceScale":5.5,"batchCount":1,"cfgZeroStar":false,"targetImageWidth":1024,"seedMode":2}"""
        # )
        config.width = 768
        config.height = 768

        # Use the Request Builder to build your image request
        req = RequestBuilder(config, "a beautiful, serene forest")

        # Pass the RequestBuilder to the service. Results are always a list of ImageBuffers
        # Since we are only generating one image, we could write this...
        # result = await service.generate(req)
        # result[0].to_file("inpaint_before.png")

        # Or we can get the first (and only) item in the results like this... (note the comma)
        (result,) = await service.generate(req)
        result.to_file("inpaint_before.png")

        # Generate a mask and save a preview
        mask = box_mask(768, 768)
        mask.to_file("inpaint_mask.png")

        # We can reuse the same RequestBuilder, and add our image and mask
        req.mask(mask)
        req.init_image("inpaint_before.png")

        # Change some settings and prompt
        req.config.strength = 0.97
        req.config["mask_blur"] = 50
        req.prompt("a raging forest fire")

        # Generate!
        result = await service.generate(req)
        result[0].to_file("inpaint_result.png")


if __name__ == "__main__":
    asyncio.run(main())
