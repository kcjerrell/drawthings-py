<!-- fullWidth: false tocVisible: false tableWrap: true -->
# drawthings-py

`drawthings-py` is a Python SDK for automating image generation with Draw Things. It provides an async client for the Draw Things gRPC service, helpers for building generation requests, reusable model/config presets, image result handling, seed utilities, and filename helpers for scripting repeatable image workflows.

The package is published as `drawthings-py` and imported as `drawthings_py`.

### Installation

Install the package with pip:

```sh
pip install drawthings-py
```

To install the package with video support, include the ffmpeg feature
```sh
pip install drawthings-py[ffmpeg]
```

`drawthings-py` requires Python 3.11 or newer.

To generate images, you will also need a running Draw Things service that accepts gRPC requests, such as the [Draw Things](https://drawthings.ai/) app or the [gRPCServerCLI](https://github.com/drawthingsai/draw-things-community). Support for the CLI is not yet released.

To use the [Draw Things](https://drawthings.ai/) app as a gRPC server, go to the advanced settings tab and enable the API server, select gRPC, and enable Transport Layer Security and Response Compression. If you are a DT+ subscriber and want to use Cloud Compute, also enable Bridge Mode.

To use the gRPCServerCLI, follow the instructions [here](https://github.com/drawthingsai/draw-things-community#self-host-grpcservercli-from-packaged-binaries).

### Basic Usage

To generate images with drawthings-py, you'll need to:

1. Connect the gRPC client
2. Load a config (either from a preset or custom)
3. Build your request with a `RequestBuilder`
4. Generate the image and save the result

```python
import asyncio
from drawthings_py import DrawThings, Configs, RequestBuilder

async def main():
    async with DrawThings.grpc() as service:
        # Load a community preset (guaranteed to work with bridge mode/DT+)
        config = Configs.from_preset("ernie_image_turbo")

        # Build your image request with prompt and negative prompt
        req = RequestBuilder(config, "An astronaut in a space helmet riding a bucking bronco on an alien planet")

        # Generate the image
        (result,) = await service.generate(req)

        # Save the result to a file
        result.to_file("astrorider.png")

asyncio.run(main())
```

### `RequestBuilder`

Regardless of whether you are using the gRPC service or the CLI, you will use a `RequestBuilder` to construct your image generation request. At a minimum, a `RequestBuilder` needs a config.

```python
from drawthings_py import RequestBuilder, Configs

config = Configs.from_preset("flux_2_klein_9b")
req = RequestBuilder(config)
```

You can assign prompts when creating the `RequestBuilder`, or set/change them later with the `prompt()` and `negative_prompt()` methods.

```python
req = RequestBuilder(config, "A firebreathing dragon", "Ugly, boring, unimpressive")
req.prompt("An icebreathing dragon")
req.negative_prompt("Ugly, boring, unimpressive, fire")
```

`RequestBuilder` instances are reusable across requests. You don't need to call a build method; the service will build the appropriate request when you call `generate()`.

```python
(result_a,) = await grpc_service.generate(req)
(result_b,) = await cli_service.generate(req)
```

(Note: the CLI service is coming soon.)

You can update properties on the config through the request's `config` property. See the Configs section for more examples.

```python
req.config["steps"] = 8
```



If you want to change to a different config, for example to alternate between different models, it's easier to use another `RequestBuilder`.

```python
req_alt = RequestBuilder(Configs.from_preset("anima_preview_3"))
```

You can add reference images, control images, or an init image for Img2Img using either a file path or an `ImageBuffer` returned from `generate()`.

```python
req.add_moodboard_image("my_character.png")
req.add_moodboard_image("awesome_outfit.png")
req.control_image("something.png", "pose")
req.init_image(gen_result)
```

Images will remain on the `RequestBuilder` until cleared.

```python
req.clear_moodboard()
req.clear_init_image()
req.clear_control_image("pose")
```

### `ImageGenerationResult`

Generated images are returned as an `ImageGenerationResult`, which is also a list of `ImageBuffer`s. If you know that only one image will be generated, you can unpack the result directly:

```python
(result,) = await service.generate(req)
```
Please note that this will raise an exception if there is more than one image in the result, for example when `batch_size` is greater than 1 or when using a video model.

Otherwise, images can be accessed by index or by iterating over the result:

```python
results = await service.generate(req)
for result in results:
    result.to_file(next_filename())
```

The `ImageGenerationResult` object also provides the generated audio (when using LTX) which can be accessed as a NumPy array and saved as a wav file.

```python
results = await service.generate(req)
if results.audio:
    results.audio.to_file("audio.wav")
```

To export a video file, first make sure the optional dependency is installed...

```sh
pip install drawthings-py[ffmpeg]
```

Then you can export a video file like this:

```python
results = await service.generate(req)
results.to_video("video.mp4", fps = 24)
```

Note: you will need to know the fps for the video model that was used. Eventually this library will be able to load model metadata, but for now you will need to be aware of the framerate for video models you use.
- Hunyuan Video: 30 fps
- LTX: 25 fps
- SkyReels: 24 fps
- Wan 2.1: 16 fps
- Wan 2.2: 16 fps



### `ImageBuffer`

Generated images are returned as a list of `ImageBuffer`s. An `ImageBuffer` contains the image's pixel data, dimensions, channel count, and any generation metadata returned by Draw Things.

You can save a generated image directly with `to_file()`:

```python
(image,) = await service.generate(req)
image.to_file("output.png")
```

Note: Images saved with the .png format will have metadata importable by Draw Things.

`ImageBuffer` can also load images from disk for use as reference, control, or init images in a `RequestBuilder`.

### `Configs`

There are a number of ways to get a config.

```python
from drawthings_py import Configs

# Load a Community Configuration preset
config = Configs.from_preset("flux_2_klein_4b")

# From JSON, as copied from the Draw Things app
config = Configs.from_json("""{"model":"z_image_turbo_1.0_q6p.ckpt","strength":1,"height":1024,"width":1024, ...}""")

# Create from scratch
config = Configs.create(width=1024, height=1024, ...)
config = Configs.create({
  "width": 768,
  "height": 768,
  ...
})
```

Change individual properties using ["item"] notation. Update many at once using .set().

```python
config["steps"] = 8
config.set({
    "width": 1024,
    "height": 1024,
})
config.set(height=1024, width=1024)
```

Loras and controlnets are exposed as lists and can be accessed and updated through their respective items. Typed helper methods are provided to add new items.

```python
config.add_lora("dmd2.ckpt", 0.5)
config["loras"][0]["weight"] = 0.25
config["loras"].clear()
```

### Seeds

Draw Things supports any seed value from 1 to 4,294,967,295, in addition to -1, which will use a random seed for each generation. This package also adds features to help manage seeds in your scripts.

**Reusable seeds** - For scripts that make multiple requests, it can sometimes be useful to use the same random seed more than once. If you use a negative value other than `-1`, a random seed will be used and saved for reuse. Any time you use the same negative value, you will get the same seed.

```python
req.config["seed"] = -2
(result_a,) = await service.generate(req) # a random seed will be chosen and assigned to -2
req.config["seed"] = -1
(result_b,) = await service.generate(req) # another random seed
req.config["seed"] = -2
(result_c,) = await service.generate(req) # this gen will have the same seed as result_a
```

(This is currently specific to an individual `RequestBuilder`)

**Deterministic seeds** - You can initialize a `RequestBuilder`'s RNG by calling `req.seed_seed(value)`, allowing you to get the same sequence of random seeds across multiple runs.

```python
req.seed_seed("example seed") # you can also use any int, float, or bytes
req.config["seed"] = -1
(result,) = await service.generate(req) # the seed is 3137907891
(result2,) = await service.generate(req) # this seed is 604582375
```

Every time you run, you will get the same sequence of seeds.

(This is also currently specific to an individual `RequestBuilder`)

**Checking a gen's seed** - If you need to see what seed was used for a gen, you can check `result.metadata["seed"]`. It will also be in the PNG metadata when the result is saved to a file.

### Filenames

You can use a `FilenamePattern` to generate filenames for your images. A `FilenamePattern` is a filename with a placeholder for a numeric counter, for example `image_####.png`. Any time the returned function is called, the specified directory will be scanned for files matching the pattern, and the highest matching filename + 1 will be returned.

```python
next_filename = FilenamePattern("image_####.png", "~/Documents/Draw Things images/")
(result,) = await service.generate(req)
result.to_file(next_filename()) # creates image_0001.png
(result,) = await service.generate(req)
result.to_file(next_filename()) # creates image_0002.png
```

This makes it easy to generate a number of images without having to worry about overwriting anything.