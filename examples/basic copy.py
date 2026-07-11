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
        config = Configs.from_json(
            """{"seedMode":2,"tiledDiffusion":false,"sampler":19,"model":"ltx_2.3_22b_distilled_q8p.ckpt","compressionArtifacts":"disabled","guidanceScale":1,"batchSize":1,"seed":3658169863,"faceRestoration":"","hiresFix":false,"maskBlurOutset":0,"refinerModel":"","loras":[],"width":512,"maskBlur":1.5,"stochasticSamplingGamma":0.29999999999999999,"compressionArtifactsQuality":43.100000000000001,"numFrames":81,"causalInferencePad":0,"cfgZeroInitSteps":0,"cfgZeroStar":true,"sharpness":0,"shift":5,"batchCount":1,"preserveOriginalAfterInpaint":true,"upscaler":"","steps":8,"controls":[],"height":384,"strength":1,"tiledDecoding":false}"""
        )

        # Use the Request Builder to build your image request
        req = RequestBuilder(
            config,
            'A man saying, "Good evening, in tonights broadcast...',
        )

        # Pass the request builder to the service
        # Results are always a list of ImageBuffers. Since we are only generating one image,
        # you can unpack the result to get the first (and only) ImageBuffer
        # (Note the parenthesis and comma)
        result = await service.generate(req)

        result.to_video("firebreathing_dragon.mp4")


if __name__ == "__main__":
    asyncio.run(main())
