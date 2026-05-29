"""Advanced usage of request builder"""

import asyncio
import re
import random

from drawthings_py import DrawThingsService, RequestBuilder, Configs


# this function will be used to process wildcards in our prompt
# prompt processors take a str, and return a str
def process_prompt(s: str) -> str:
    def replace(match):
        options = match.group(1).split("|")
        return random.choice(options).strip()

    return re.sub(r"\[([^\[\]]+)\]", replace, s)


async def main():
    """Editing with Klein"""
    async with DrawThingsService.grpc("127.0.0.1", 7859) as service:
        # load a community preset
        config = Configs.from_preset("flux_2_klein_4b")

        # set up our request builder with our Klein 4b config
        req = RequestBuilder(config)

        # attach our prompt processor to handle the wildcards in our prompts
        req.prompt_processor(process_prompt)

        # reduce size for faster results
        req.config["width"] = 768
        req.config["height"] = 768

        # when this request is sent, the prompt processer will randomly choose one value in each set
        req.prompt(
            "photo of a man in front of a gray background. "
            "He has [wild|short|neat|curly] [red|blonde|black|neon green] hair "
            "and [an eyepatch over his left eye|a bushy beard|a visor over his eyes|facial tattoos]. "
            "He is wearing a plain white t-shirt"
        )
        result_first_man = await service.generate_image(req)
        result_first_man[0].to_file("example_klein_first_man.png")
        print(f"Generated image: {result_first_man[0].prompt}")

        # there is a 1/64 chance that these two prompts will end up being the same
        result_second_man = await service.generate_image(req)
        result_second_man[0].to_file("example_klein_second_man.png")
        print(f"Generated image: {result_second_man[0].prompt}")

        req.prompt(
            "photo of [an avante-garde|a japenese-inspired|a futuristic] [leather|latex|denim] men's suit "
            "displayed on a mannequin in front of a gray background"
        )
        results_suit = await service.generate_image(req)
        results_suit[0].to_file("example_klein_suit.png")
        print(f"Generated image: {results_suit[0].prompt}")

        req.prompt(
            "show both of these men, each wearing this suit, walking the runway at a fashion show"
        )

        # add images by path
        req.add_moodboard_image("example_klein_first_man.png")
        req.add_moodboard_image("example_klein_second_man.png")

        # or add images directly from request result
        req.add_moodboard_image(results_suit[0])

        # increase resolution for final image
        # req.config["width"] = 1024
        # req.config["height"] = 1024

        results_final = await service.generate_image(req)
        results_final[0].to_file("example_klein_final.png")
        print(f"Generated image: {results_final[0].prompt}")

        # moodboard images will remain on the request builder until cleared
        req.clear_moodboard()

        req.add_moodboard_image("example_klein_final.png")
        req.prompt(
            "While keeping the identities of the men and the design of the suit the same, "
            "Show this scene from a 3/4 view, close-up, looking slightly upward at the men's faces"
        )

        results_closeup = await service.generate_image(req)
        results_closeup[0].to_file("example_klein_closeup.png")
        print(f"Generated image: {results_closeup[0].prompt}")


if __name__ == "__main__":
    asyncio.run(main())
