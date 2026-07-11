"""
Generation and editing with Klein 4b
with advanced usage of the RequestBuilder

You can run this script locally with Klein 4b (6-bit)
(flux_2_klein_4b_q6p.ckpt), or with DT+ and bridge mode.
"""

import asyncio
import re
import random

from drawthings_py import DrawThings, RequestBuilder, Configs


# this function will be used to process wildcards in our prompt
# prompt processors take a str, and return a str
def process_prompt(s: str) -> str:
    def replace(match: re.Match[str]) -> str:
        options = match.group(1).split("|")
        return random.choice(options).strip()

    return re.sub(r"\[([^\[\]]+)\]", replace, s)


async def main():
    """Editing with Klein"""
    async with DrawThings.grpc("127.0.0.1", 7859) as service:
        # load a community preset
        config = Configs.from_preset("flux_2_klein_4b")

        # set up our request builder with our Klein 4b config
        req = RequestBuilder(config)

        # reduce size for faster results
        req.config.width = 768
        req.config.height = 768

        # attach our prompt processor to handle the wildcards in our prompts
        req.prompt_processor(process_prompt)

        # Set the prompt. The prompt processor will select one option from each set
        req.prompt(
            "Photo of a man in front of a gray background. "
            "He has [wild|short|neat|curly] [red|blonde|black|neon green] hair "
            "and [an eyepatch over his left eye|a bushy beard|a visor over his eyes|facial tattoos]. "
            "He is wearing a plain white t-shirt"
        )

        # Generate the image.
        result_first_man = await service.generate(req)
        result_first_man[0].to_file("example_klein_first_man.png")
        print(f"Generated image: {result_first_man[0].prompt}")

        # Generate another image. The prompt processor will run again, selecting different options
        # (There is a 1/64 chance it will pick all the same options)
        result_second_man = await service.generate(req)
        result_second_man[0].to_file("example_klein_second_man.png")
        print(f"Generated image: {result_second_man[0].prompt}")

        # Generate a suit image
        req.prompt(
            "Photo of [an avante-garde|a Japenese-inspired|a futuristic] [leather|latex|denim] men's suit "
            "displayed on a mannequin in front of a gray background."
        )
        results_suit = await service.generate(req)
        results_suit[0].to_file("example_klein_suit.png")
        print(f"Generated image: {results_suit[0].prompt}")

        # Generate a final image showing both men in the suit
        req.prompt(
            "Show both of these men, each wearing this suit, walking the runway at a fashion show."
        )

        # For Klein and other edit models, we use the moodboard for reference images
        # We can add them by path...
        req.add_moodboard_image("example_klein_first_man.png")
        req.add_moodboard_image("example_klein_second_man.png")

        # ...or images directly from a previous request's result
        req.add_moodboard_image(results_suit[0])

        # Generate the combined image
        results_final = await service.generate(req)
        results_final[0].to_file("example_klein_final.png")
        print(f"Generated image: {results_final[0].prompt}")

        # Just like in Draw Things, moodboard images will remain until cleared
        req.clear_moodboard()

        # Let's get another angle
        req.add_moodboard_image("example_klein_final.png")
        req.prompt(
            "While keeping the identities of the men and the design of the suit the same, "
            "Show this scene from a 3/4 view, close-up, looking slightly upward at the men's faces"
        )

        results_closeup = await service.generate(req)
        results_closeup[0].to_file("example_klein_closeup.png")
        print(f"Generated image: {results_closeup[0].prompt}")


if __name__ == "__main__":
    asyncio.run(main())
