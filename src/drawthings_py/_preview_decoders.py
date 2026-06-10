import fpzip
import numpy as np
from .image_buffer import ImageBuffer


def clamp(value: int) -> int:
    return max(min(int(value if np.isfinite(value) else 0), 255), 0)


def decode_preview(preview: bytes, version: str | None = None) -> ImageBuffer | None:
    width, height, channels, floats = get_image_data(preview)

    if version is not None:
        version = version.lower()

    if version:
        if (
            version.startswith("flux1")
            or version.startswith("hidream")
            or version.startswith("zimage")
            or version.startswith("flux")
        ) and not version.startswith("flux2"):
            return decode_flux(width, height, floats)

        if version.startswith("flux2"):
            return decode_flux2(width, height, floats)

        if version.startswith("sd3"):
            return decode_sd3(width, height, floats)

        if version.startswith("sdxl") or version in ("ssd1b", "pixart", "auraflow"):
            return decode_sdxl(width, height, floats)

        if (
            version.startswith("v1")
            or version.startswith("v2")
            or version.startswith("svdi2v")
        ):
            return decode_v1_v2(width, height, floats)

        if version.startswith("wan2.1") or version.startswith("qwen"):
            return decode_wan2_1(width, height, floats)

        if version.startswith("wan2.2"):
            return decode_wan2_2(width, height, floats)

        if version == "hunyuanvideo":
            return decode_hunyuanvideo(width, height, floats)

        if version.startswith("wurst"):
            return decode_wurst(width, height, floats, channels)

    # Dynamic fallbacks based on channel count when version is None (or not matched)
    if channels == 16:
        # Default fallback for 16 channels is Flux
        return decode_flux(width, height, floats)
    elif channels == 4:
        # Default fallback for 4 channels is SDXL
        return decode_sdxl(width, height, floats)
    elif channels == 32:
        return decode_flux2(width, height, floats)
    elif channels == 48:
        return decode_wan2_2(width, height, floats)
    elif channels == 3:
        return decode_wurst(width, height, floats, channels)

    print("couldn't decode preview")
    return None


def get_image_data(response_image: bytes) -> tuple[int, int, int, np.ndarray]:
    int_buffer = np.frombuffer(response_image, dtype=np.uint32, count=17)

    height, width, channels = int_buffer[6:9]  # pyright: ignore [reportAny]
    length = width * height * channels * 2  # pyright: ignore [reportAny]
    is_compressed = int_buffer[0] == 1012247  # pyright: ignore [reportAny]

    if is_compressed:
        uncompressed: np.ndarray = fpzip.decompress(response_image[68:], order="C")  # pyright: ignore [reportUnknownMemberType, reportUnknownVariableType]
        buffer = uncompressed.astype(np.float16).tobytes()  # pyright: ignore [reportUnknownMemberType, reportUnknownVariableType]
    else:
        buffer = response_image[68:]

    floats = np.frombuffer(buffer, dtype=np.float16, count=length // 2)  # pyright: ignore [reportUnknownArgumentType, reportAny]

    return (width, height, channels, floats)


def is_flux_type(version: str | None):
    if version is None:
        return False
    if (
        version.startswith("flux1")
        or version.startswith("hidream")
        or version.startswith("zimage")
    ):
        return True
    return False


def decode_flux(width: int, height: int, data: np.ndarray) -> ImageBuffer:
    v = data.reshape(-1, 16)
    W = np.array(
        [
            [-0.0346, 0.0244, 0.0681],
            [0.0034, 0.0210, 0.0687],
            [0.0275, -0.0668, -0.0433],
            [-0.0174, 0.0160, 0.0617],
            [0.0859, 0.0721, 0.0329],
            [0.0004, 0.0383, 0.0115],
            [0.0405, 0.0861, 0.0915],
            [-0.0236, -0.0185, -0.0259],
            [-0.0245, 0.0250, 0.1180],
            [0.1008, 0.0755, -0.0421],
            [-0.0515, 0.0201, 0.0011],
            [0.0428, -0.0012, -0.0036],
            [0.0817, 0.0765, 0.0749],
            [-0.1264, -0.0522, -0.1103],
            [-0.0280, -0.0881, -0.0499],
            [-0.1262, -0.0982, -0.0778],
        ],
        dtype=np.float32,
    )
    bias = np.array([-0.0329, -0.0718, -0.0851], dtype=np.float32)

    rgb = (v @ W + bias) * 127.5 + 127.5
    rgb = np.clip(rgb, 0, 255).astype(np.uint8)

    rgba = np.empty((width * height, 4), dtype=np.uint8)
    rgba[:, :3] = rgb
    rgba[:, 3] = 255

    return ImageBuffer(
        data=rgba.tobytes(),
        width=width,
        height=height,
        channels=4,
    )


def decode_v1_v2(width: int, height: int, data: np.ndarray) -> ImageBuffer:
    v = data.reshape(-1, 4)
    W = np.array(
        [
            [49.5210, 41.1373, 40.2919],
            [29.0283, 42.4951, 18.9304],
            [-23.9673, 24.7349, 30.0236],
            [-39.4981, -50.8279, -81.9976],
        ],
        dtype=np.float32,
    )
    bias = np.array([99.9368, 99.8421, 99.5384], dtype=np.float32)

    rgb = v @ W + bias
    rgb = np.clip(rgb, 0, 255).astype(np.uint8)

    rgba = np.empty((width * height, 4), dtype=np.uint8)
    rgba[:, :3] = rgb
    rgba[:, 3] = 255

    return ImageBuffer(
        data=rgba.tobytes(),
        width=width,
        height=height,
        channels=4,
    )


def decode_sd3(width: int, height: int, data: np.ndarray) -> ImageBuffer:
    v = data.reshape(-1, 16)
    W = np.array(
        [
            [-0.0922, -0.0175, 0.0749],
            [0.0311, 0.0633, 0.0954],
            [0.1994, 0.0927, 0.0458],
            [0.0856, 0.0339, 0.0902],
            [0.0587, 0.0272, -0.0496],
            [-0.0006, 0.1104, 0.0309],
            [0.0978, 0.0306, 0.0427],
            [-0.0042, 0.1038, 0.1358],
            [-0.0194, 0.0020, 0.0669],
            [-0.0488, 0.0130, -0.0268],
            [0.0922, 0.0988, 0.0951],
            [-0.0278, 0.0524, -0.0542],
            [0.0332, 0.0456, 0.0895],
            [-0.0069, -0.0030, -0.0810],
            [-0.0596, -0.0465, -0.0293],
            [-0.1448, -0.1463, -0.1189],
        ],
        dtype=np.float32,
    )
    bias = np.array([0.2394, 0.2135, 0.1925], dtype=np.float32)

    rgb = (v @ W + bias) * 127.5 + 127.5
    rgb = np.clip(rgb, 0, 255).astype(np.uint8)

    rgba = np.empty((width * height, 4), dtype=np.uint8)
    rgba[:, :3] = rgb
    rgba[:, 3] = 255

    return ImageBuffer(
        data=rgba.tobytes(),
        width=width,
        height=height,
        channels=4,
    )


def decode_sdxl(width: int, height: int, data: np.ndarray) -> ImageBuffer:
    v = data.reshape(-1, 4)
    W = np.array(
        [
            [47.195, 53.237, 58.182],
            [-29.114, -1.4623, 4.3734],
            [11.883, 12.991, -3.3735],
            [-38.063, -28.043, -26.722],
        ],
        dtype=np.float32,
    )
    bias = np.array([141.64, 127.46, 114.5], dtype=np.float32)

    rgb = v @ W + bias
    rgb = np.clip(rgb, 0, 255).astype(np.uint8)

    rgba = np.empty((width * height, 4), dtype=np.uint8)
    rgba[:, :3] = rgb
    rgba[:, 3] = 255

    return ImageBuffer(
        data=rgba.tobytes(),
        width=width,
        height=height,
        channels=4,
    )


def decode_wan2_1(width: int, height: int, data: np.ndarray) -> ImageBuffer:
    v = data.reshape(-1, 16)
    W = np.array(
        [
            [-0.1299, -0.1692, 0.2932],
            [0.0671, 0.0406, 0.0442],
            [0.3568, 0.2548, 0.1747],
            [0.0372, 0.2344, 0.1420],
            [0.0313, 0.0189, -0.0328],
            [0.0296, -0.0956, -0.0665],
            [-0.3477, -0.4059, -0.2925],
            [0.0166, 0.1902, 0.1975],
            [-0.0412, 0.0267, -0.1364],
            [-0.1293, 0.0740, 0.1636],
            [0.0680, 0.3019, 0.1128],
            [0.0032, 0.0581, 0.0639],
            [-0.1251, 0.0927, 0.1699],
            [0.0060, -0.0633, 0.0005],
            [0.3477, 0.2275, 0.2950],
            [0.1984, 0.0913, 0.1861],
        ],
        dtype=np.float32,
    )
    bias = np.array([-0.1835, -0.0868, -0.336], dtype=np.float32)

    rgb = (v @ W + bias) * 127.5 + 127.5
    rgb = np.clip(rgb, 0, 255).astype(np.uint8)

    rgba = np.empty((width * height, 4), dtype=np.uint8)
    rgba[:, :3] = rgb
    rgba[:, 3] = 255

    return ImageBuffer(
        data=rgba.tobytes(),
        width=width,
        height=height,
        channels=4,
    )


def decode_wan2_2(width: int, height: int, data: np.ndarray) -> ImageBuffer:
    v = data.reshape(-1, 48)
    W_r = np.array(
        [
            0.0119,
            -0.1062,
            0.0140,
            -0.0813,
            0.0656,
            0.0264,
            0.0295,
            -0.0244,
            0.0443,
            -0.0465,
            0.0359,
            -0.0776,
            0.0564,
            0.0006,
            -0.0319,
            -0.0268,
            0.0539,
            -0.0359,
            -0.0285,
            0.1041,
            -0.0086,
            0.0390,
            0.0069,
            0.0006,
            0.0313,
            -0.1454,
            0.0714,
            -0.0304,
            0.0401,
            -0.0758,
            0.0568,
            -0.0055,
            0.0239,
            -0.0663,
            -0.0416,
            0.0166,
            -0.0211,
            0.1833,
            -0.0368,
            -0.3441,
            -0.0479,
            -0.0660,
            -0.0101,
            -0.0690,
            -0.0145,
            0.0421,
            0.0504,
            -0.0837,
        ],
        dtype=np.float32,
    )
    W_g = np.array(
        [
            0.0103,
            -0.0504,
            0.0409,
            -0.0677,
            0.0851,
            0.0463,
            0.0326,
            -0.0270,
            -0.0102,
            -0.0090,
            0.0236,
            0.0854,
            0.0264,
            0.0594,
            -0.0542,
            0.0024,
            0.0265,
            -0.0312,
            -0.1032,
            0.0537,
            -0.0374,
            0.0670,
            0.0144,
            -0.0167,
            -0.0574,
            -0.0902,
            0.0827,
            -0.0574,
            0.0384,
            -0.0297,
            0.1307,
            -0.0310,
            -0.0305,
            -0.0673,
            -0.0047,
            0.0112,
            0.0011,
            0.1466,
            0.0370,
            -0.3543,
            -0.0489,
            -0.0153,
            0.0068,
            -0.0452,
            0.0041,
            0.0451,
            -0.0483,
            0.0168,
        ],
        dtype=np.float32,
    )
    W_b = np.array(
        [
            0.0046,
            0.0165,
            0.0491,
            0.0607,
            0.0808,
            0.0912,
            0.0590,
            0.0025,
            0.0288,
            -0.0205,
            0.0082,
            0.1048,
            0.0561,
            0.0418,
            -0.0637,
            0.0260,
            0.0358,
            -0.0287,
            -0.1237,
            0.0622,
            -0.0051,
            0.2863,
            0.0082,
            0.0079,
            -0.0232,
            -0.0481,
            0.0447,
            -0.0196,
            0.0204,
            -0.0014,
            0.1372,
            -0.0380,
            0.0325,
            -0.0140,
            -0.0023,
            -0.0093,
            0.0331,
            0.2250,
            0.0295,
            -0.2008,
            -0.0420,
            0.0800,
            0.0156,
            -0.0927,
            0.0015,
            0.0373,
            -0.0356,
            0.0055,
        ],
        dtype=np.float32,
    )
    W = np.stack([W_r, W_g, W_b], axis=-1)

    rgb = (v @ W) * 127.5 + 127.5
    rgb = np.clip(rgb, 0, 255).astype(np.uint8)

    rgba = np.empty((width * height, 4), dtype=np.uint8)
    rgba[:, :3] = rgb
    rgba[:, 3] = 255

    return ImageBuffer(
        data=rgba.tobytes(),
        width=width,
        height=height,
        channels=4,
    )


def decode_hunyuanvideo(width: int, height: int, data: np.ndarray) -> ImageBuffer:
    v = data.reshape(-1, 16)
    W = np.array(
        [
            [-0.0395, -0.0331, 0.0445],
            [0.0696, 0.0795, 0.0518],
            [0.0135, -0.0945, -0.0282],
            [0.0108, -0.0250, -0.0765],
            [-0.0209, 0.0032, 0.0224],
            [-0.0804, -0.0254, -0.0639],
            [-0.0991, 0.0271, -0.0669],
            [-0.0646, -0.0422, -0.0400],
            [-0.0696, -0.0595, -0.0894],
            [-0.0799, -0.0208, -0.0375],
            [0.1166, 0.1627, 0.0962],
            [0.1165, 0.0432, 0.0407],
            [-0.2315, -0.1920, -0.1355],
            [-0.0270, 0.0401, -0.0821],
            [-0.0616, -0.0997, -0.0727],
            [0.0249, -0.0469, -0.1703],
        ],
        dtype=np.float32,
    )
    bias = np.array([0.0249, -0.0192, -0.0761], dtype=np.float32)

    rgb = (v @ W + bias) * 127.5 + 127.5
    rgb = np.clip(rgb, 0, 255).astype(np.uint8)

    rgba = np.empty((width * height, 4), dtype=np.uint8)
    rgba[:, :3] = rgb
    rgba[:, 3] = 255

    return ImageBuffer(
        data=rgba.tobytes(),
        width=width,
        height=height,
        channels=4,
    )


def decode_wurst(
    width: int, height: int, data: np.ndarray, channels: int
) -> ImageBuffer:
    if channels == 3:
        v = data.reshape(-1, 3)
        rgb = np.clip(v, 0, 255).astype(np.uint8)
    else:
        v = data.reshape(-1, 4)
        W = np.array(
            [
                [10.175, 21.07, 7.8454],
                [-20.807, -4.3022, -2.3713],
                [-27.834, -11.258, -0.45565],
                [-2.0577, -18.8, -41.648],
            ],
            dtype=np.float32,
        )
        bias = np.array([143.39, 131.53, 120.76], dtype=np.float32)

        rgb = v @ W + bias
        rgb = np.clip(rgb, 0, 255).astype(np.uint8)

    rgba = np.empty((width * height, 4), dtype=np.uint8)
    rgba[:, :3] = rgb
    rgba[:, 3] = 255

    return ImageBuffer(
        data=rgba.tobytes(),
        width=width,
        height=height,
        channels=4,
    )


def decode_flux2(width: int, height: int, data: np.ndarray) -> ImageBuffer:
    v = data.reshape(-1, 32)
    W_r = np.array(
        [
            0.0058,
            0.0495,
            -0.0099,
            0.2144,
            0.0166,
            0.0157,
            -0.0398,
            -0.0052,
            -0.3527,
            -0.0301,
            -0.0107,
            0.0746,
            0.0156,
            -0.0034,
            0.0032,
            -0.0939,
            0.0018,
            0.0284,
            -0.0024,
            0.1207,
            0.0128,
            0.0137,
            0.0095,
            0.0000,
            -0.0465,
            0.0095,
            0.0290,
            0.0220,
            -0.0332,
            -0.0085,
            -0.0076,
            -0.0111,
        ],
        dtype=np.float32,
    )
    W_g = np.array(
        [
            0.0113,
            0.0443,
            0.0096,
            0.3009,
            -0.0039,
            0.0103,
            0.0902,
            0.0095,
            -0.2712,
            -0.0356,
            0.0078,
            0.0090,
            0.0169,
            -0.0040,
            0.0181,
            -0.0008,
            0.0043,
            0.0056,
            -0.0022,
            -0.0026,
            0.0101,
            -0.0072,
            0.0092,
            -0.0077,
            -0.0204,
            0.0012,
            -0.0034,
            0.0169,
            -0.0457,
            0.0389,
            0.0003,
            -0.0460,
        ],
        dtype=np.float32,
    )
    W_b = np.array(
        [
            0.0073,
            0.0836,
            0.0644,
            0.3652,
            -0.0054,
            -0.0160,
            -0.0235,
            0.0109,
            -0.1666,
            -0.0180,
            0.0013,
            -0.0941,
            0.0070,
            -0.0114,
            0.0080,
            0.0186,
            0.0104,
            -0.0127,
            -0.0030,
            0.0065,
            0.0142,
            -0.0007,
            -0.0059,
            -0.0049,
            -0.0312,
            -0.0066,
            0.0025,
            -0.0048,
            -0.0468,
            0.0609,
            -0.0043,
            -0.0614,
        ],
        dtype=np.float32,
    )
    W = np.stack([W_r, W_g, W_b], axis=-1)
    bias = np.array([-0.0329, -0.0718, -0.0851], dtype=np.float32)

    rgb = (v @ W + bias) * 127.5 + 127.5
    rgb = np.clip(rgb, 0, 255).astype(np.uint8)

    rgba = np.empty((width * height, 4), dtype=np.uint8)
    rgba[:, :3] = rgb
    rgba[:, 3] = 255

    return ImageBuffer(
        data=rgba.tobytes(),
        width=width,
        height=height,
        channels=4,
    )
