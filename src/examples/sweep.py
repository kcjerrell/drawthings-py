import asyncio
from os import path
from drawthings_py import DrawThingsService, Configs, RequestBuilder
from drawthings_py.util import next_batch_pattern, next_filename, get_seed

# create a config from Draw Thing's "Copy config"
# config = Configs.from_json(
#     """{"maskBlurOutset":0,"causalInferencePad":0,"tiledDecoding":false,"negativeOriginalImageWidth":512,"model":"illustrij_genv1_q6p_q8p.ckpt","maskBlur":2.5,"negativeAestheticScore":2.5,"seed":-1,"height":768,"upscaler":"","faceRestoration":"","steps":16,"clipSkip":2,"targetImageHeight":768,"sharpness":0,"guidanceScale":5,"aestheticScore":6,"targetImageWidth":768,"tiledDiffusion":false,"width":768,"cropLeft":0,"batchSize":1,"cropTop":0,"batchCount":1,"negativeOriginalImageHeight":512,"preserveOriginalAfterInpaint":true,"cfgZeroInitSteps":0,"zeroNegativePrompt":true,"controls":[],"seedMode":2,"hiresFix":false,"refinerModel":"","shift":1,"originalImageWidth":768,"loras":[],"cfgZeroStar":false,"originalImageHeight":768,"sampler":12,"strength":1}"""
# )

config = Configs.from_preset("z_image_base")
config["width"] = 768
config["height"] = 512

# create a filename pattern for this batch of images
# the first time you run this script, the pattern will be ./batch_01_img_##.png
batch_pattern = next_batch_pattern("batch_$$_img_##.png", ".")


async def main():
    async with DrawThingsService.grpc() as service:
        req = RequestBuilder(config, "an ice dragon")
        
        # we want to use the same seed for the whole batch, so we use get_seed()
        # if we left seed at -1, it would use a different seed for every image
        req.config["seed"] = get_seed()

        req.prompt("an ice dragon, and lots of keywords like awesome, high quality, masterpiece")
        req.negative_prompt("ugly, low quality, fire, cat")

        for i in range(4):
            # we will see how the image looks with CFG at 2, 4, 6, and 8
            req.config["guidance_scale"] = 2 + 2 * i
            result = await service.generate_image(req)
            
            # save the result, using the same filename pattern for safely incrementing filenames
            result[0].to_file(next_filename(batch_pattern))


if __name__ == "__main__":
    asyncio.run(main())
