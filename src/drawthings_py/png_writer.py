import io
import json
import struct
import zlib
from PIL import Image

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def png_chunk(chunk_type: bytes, data: bytes) -> bytes:
    crc = zlib.crc32(chunk_type)
    crc = zlib.crc32(data, crc)

    return (
        struct.pack(">I", len(data))
        + chunk_type
        + data
        + struct.pack(">I", crc & 0xFFFFFFFF)
    )


def build_itxt_chunk(keyword: str, text: str) -> bytes:
    out = bytearray()

    out.extend(keyword.encode("utf-8"))
    out.append(0)  # keyword null terminator

    out.append(0)  # compression flag
    out.append(0)  # compression method

    out.append(0)  # language tag empty
    out.append(0)  # translated keyword empty

    out.extend(text.encode("utf-8"))

    return bytes(out)


def build_exif_user_comment(width: int, height: int) -> bytes:
    exif = bytearray()

    # TIFF header
    exif.extend(b"MM")  # big endian
    exif.extend(struct.pack(">H", 42))
    exif.extend(struct.pack(">I", 8))

    # IFD0
    exif.extend(struct.pack(">H", 1))

    # ExifOffset tag
    exif.extend(struct.pack(">H", 0x8769))
    exif.extend(struct.pack(">H", 4))  # LONG
    exif.extend(struct.pack(">I", 1))
    exif.extend(struct.pack(">I", 26))

    # next IFD
    exif.extend(struct.pack(">I", 0))

    # Exif SubIFD
    exif.extend(struct.pack(">H", 2))

    # ExifImageWidth
    exif.extend(struct.pack(">H", 0xA002))
    exif.extend(struct.pack(">H", 4))
    exif.extend(struct.pack(">I", 1))
    exif.extend(struct.pack(">I", width))

    # ExifImageHeight
    exif.extend(struct.pack(">H", 0xA003))
    exif.extend(struct.pack(">H", 4))
    exif.extend(struct.pack(">I", 1))
    exif.extend(struct.pack(">I", height))

    # next SubIFD
    exif.extend(struct.pack(">I", 0))

    return bytes(exif)


def format_desc_float(f: float) -> str:
    s = str(float(f))

    if "." not in s:
        return s + ".0"

    return s


def build_description(metadata: dict | None) -> str:
    if metadata is None:
        return ""

    return (
        f"{metadata['c']}\n"
        f"-{metadata['uc']}\n"
        f"Steps: {metadata['steps']}, "
        f"Sampler: {metadata['sampler']}, "
        f"Guidance Scale: {format_desc_float(metadata['v2']['guidanceScale'])}, "
        f"Seed: {metadata['seed']}, "
        f"Size: {metadata['size']}, "
        f"Model: {metadata['model']}, "
        f"Strength: {format_desc_float(metadata['strength'])}, "
        f"Seed Mode: {metadata['seed_mode']}, "
        f"Shift: {format_desc_float(metadata['shift'])}"
    )


def build_drawthings_xmp(json_string: str, description: str) -> str:
    escaped_description = description.replace("\n", "&#xA;")

    return f"""<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="XMP Core 6.0.0">
    <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
        <rdf:Description rdf:about=""
            xmlns:dc="http://purl.org/dc/elements/1.1/"
            xmlns:xmp="http://ns.adobe.com/xap/1.0/"
            xmlns:exif="http://ns.adobe.com/exif/1.0/">
            <dc:description>
                <rdf:Alt>
                    <rdf:li xml:lang="x-default">{escaped_description}</rdf:li>
                </rdf:Alt>
            </dc:description>
            <xmp:CreatorTool>Draw Things</xmp:CreatorTool>
            <exif:UserComment>
                <rdf:Alt>
                    <rdf:li xml:lang="x-default">{json_string}</rdf:li>
                </rdf:Alt>
            </exif:UserComment>
      </rdf:Description>
   </rdf:RDF>
</x:xmpmeta>
"""


def write_png_with_usercomment(
    pixels: bytes,
    width: int,
    height: int,
    channels: int,
    metadata: dict | None = None,
) -> bytes:
    mode_map = {
        1: "L",
        2: "LA",
        3: "RGB",
        4: "RGBA",
    }

    if channels not in mode_map:
        raise ValueError("Unsupported channel count")

    mode = mode_map[channels]

    img = Image.frombytes(mode, (width, height), pixels)

    temp = io.BytesIO()
    img.save(temp, format="PNG")

    png_data = temp.getvalue()

    # Parse existing PNG chunks
    pos = 8
    chunks = []

    while pos < len(png_data):
        length = struct.unpack(">I", png_data[pos : pos + 4])[0]
        chunk_type = png_data[pos + 4 : pos + 8]
        chunk_data = png_data[pos + 8 : pos + 8 + length]
        chunk_crc = png_data[pos + 8 + length : pos + 12 + length]

        chunks.append(
            (
                chunk_type,
                chunk_data,
                chunk_crc,
            )
        )

        pos += length + 12

    out = bytearray()
    out.extend(PNG_SIGNATURE)

    inserted = False

    for chunk_type, chunk_data, chunk_crc in chunks:
        out.extend(
            struct.pack(">I", len(chunk_data)) + chunk_type + chunk_data + chunk_crc
        )

        if chunk_type == b"IHDR" and not inserted:
            # sRGB chunk
            out.extend(
                png_chunk(
                    b"sRGB",
                    b"\x00",
                )
            )

            if metadata is not None:
                json_string = json.dumps(metadata, indent=2)

                exif = build_exif_user_comment(width, height)

                out.extend(
                    png_chunk(
                        b"eXIf",
                        exif,
                    )
                )

                xmp = build_drawthings_xmp(
                    json_string,
                    build_description(metadata),
                )

                itxt = build_itxt_chunk(
                    "XML:com.adobe.xmp",
                    xmp,
                )

                out.extend(
                    png_chunk(
                        b"iTXt",
                        itxt,
                    )
                )

            inserted = True

    return bytes(out)
