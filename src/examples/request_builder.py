"""
(Nearly) minimal example of using the Draw Things service.
"""

import asyncio
import random
import re

from drawthings_py import DrawThingsService, Configs, RequestBuilder


async def main():
    """
    Generate a single image using the Draw Things service.
    """

    if "this example isn't really meant to be run as a script":
        return

    async with DrawThingsService.grpc() as service:
        # Loading a community preset
        # Presets are all guaranteed to work with bridge mode (DT+)
        config = Configs.from_preset("flux_2_klein_9b")

        # The RequestBuilder is used to craft our image generation requests

        # At a minimum, it needs a config.
        req = RequestBuilder(config)

        # You can update the request's config
        req.config["steps"] = 8
        req.config["loras"].append({"file": "byol.safetensors", "weight": 1.0})

        # If you wanted to change to a different config, for example to alternate between
        # different models, its easier to just use another RequestBuilder.
        reqAlt = RequestBuilder(Configs.from_preset("anima_preview_3"))

        # You can add reference images to use with an edit model
        req.add_moodboard_image("my_character.png")
        req.add_moodboard_image("awesome_outfit.png")

        req.prompt("Show this man wearing this snazzy outfit")

        char_in_costume = await service.generate_image(req)
        char_in_costume[0].to_file("char_in_costume.png")

        # RequestBuilders are reusable. The moodboard images are still there
        req.prompt("Show this man wearing this snazzy outfit at a party")

        char_at_party = await service.generate_image(req)
        char_at_party[0].to_file("char_at_party.png")

        # If you like fluent style, you can do that too. Every method modifies and returns the request
        req = (
            req.clear_moodboard()
            .init_image(char_at_party[0])
            .prompt("Enhance the quality and detail of this image")
            .update_config({"width": 1280, "height": 1280})
        )

        # this function will pick a random option from a wildcard set
        def process_prompt(s: str) -> str:
            def replace(match):
                options = match.group(1).split("|")
                return random.choice(options).strip()

            return re.sub(r"\[([^\[\]]+)\]", replace, s)

        req.prompt_processor(process_prompt)

        req.prompt(
            "Show this man wearing [a suit|a police uniform|a safari outfit|not much] "
            "and driving [a monster truck|a speedboat|me crazy]"
        )

        for i in range(3):
            # the prompt processor will pick new values for each request
            result = await service.generate_image(req)
            result[0].to_file(f"wildcard_{i}.png")


if __name__ == "__main__":
    asyncio.run(main())
