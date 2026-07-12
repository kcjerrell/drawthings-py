"""
Generating video
"""

import asyncio

from drawthings_py import DrawThings, Configs, FilenamePattern, RequestBuilder


async def main():
    """
    Generating a video with LTX 2.3 distilled
    """
    async with DrawThings.grpc() as service:
        # Use the ltx 2.3 distilled preset
        config = Configs.from_preset("ltx_2_3_distilled")

        # Reduce size and length for example
        config["width"] = 640
        config["height"] = 368
        config["num_frames"] = 81
        config["hires_fix"] = False

        # Use the Request Builder to build the request
        req = RequestBuilder(
            config,
            'A man saying, "Good evening, in tonights broadcast...',
        )

        # Pass the request builder to the service
        # It may take a while for the result to be downloaded if using DT+
        result = await service.generate(req)

        # You can save individual frames by iterating through the result
        # you can use a FilenamePattern to automatically number the frames
        next_filename = FilenamePattern("f_###.png", "./tonights_broadcast_frames")
        for frame in result:
            frame.to_file(next_filename())

        # If the model generates audio it will be on the result as well
        # Check for None just to be safe
        if result.audio is not None:
            result.audio.to_file("tonights_broadcast_audio.wav")

        # If you have installed the optional ffmpeg dependency, you can save a video
        # install with `pip install "drawthings-py[ffmpeg]"`
        result.to_video("tonights_broadcast.mp4", fps=25)


if __name__ == "__main__":
    asyncio.run(main())
