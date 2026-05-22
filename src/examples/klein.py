"""Basic image generation with Flux2 Klein 4b"""

import asyncio

from drawthings_py import RequestBuilder, DrawThingsService, Config

config = Config(
    {
        "model": "flux_2_klein_4b_q6p.ckpt",
        "width": 768,
        "height": 768,
        "seed": -1,
        "strength": 1,
        "steps": 4,
        "guidanceScale": 1,
        "sampler": "UniPCTrailing",
        "shift": 3,
    }
)


async def main():
    """Editing with Klein"""
    async with DrawThingsService.grpc("127.0.0.1", 7859) as service:
        req = RequestBuilder(
            config,
            "photo of a man in front of a gray background, from the shoulders up, distinct facial features",
        )
        req.on_preview(lambda img, step: img.to_file(f"img_man_{step}.png"))
        results_man = await service.generate_image(req)
        results_man[0].to_file("img_man.png")

        req = RequestBuilder(
            config, "photo of a fashionable, futuristic men's suit, product image"
        )
        results_suit = await service.generate_image(req)
        results_suit[0].to_file("img_suit.png")

        req = RequestBuilder(
            config,
            "show this man wearing the suit",
        )

        # add images by path
        req.init_image("img_suit.png")
        # add images by from request result
        req.add_moodboard_image(results_man[0])

        results_combined = await service.generate_image(req)
        results_combined[0].to_file("img_combined.png")


if __name__ == "__main__":
    asyncio.run(main())
