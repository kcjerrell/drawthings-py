"""
How to list available models
"""

import asyncio

from drawthings_py import DrawThings


async def main():
    """
    Generate a single image using the Draw Things service.
    Note: gRPC server must have Model Browser enabled.
    """
    async with DrawThings.grpc() as service:
        models = await service.get_models()

        print(
            f"Server has {len(models.models)} models, {len(models.loras)} loras, and {len(models.controlNets)} controlnets"
        )

        print(", ".join([model.name for model in models.models]))


if __name__ == "__main__":
    asyncio.run(main())
