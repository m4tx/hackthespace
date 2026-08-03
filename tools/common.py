"""Shared helpers for the one-off puzzle asset generators.

De-Django-ified versions of the old ``game/utils/{images,files}.py`` helpers.
"""
import os
from random import randint

from PIL import Image, ImageDraw, ImageFont

# The Roboto font shipped with the Rust project (used by build.rs too).
FONT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "assets", "fonts",
)


def font_path(font_name: str) -> str:
    """Resolve a font file name against the project's ``assets/fonts`` dir."""
    return os.path.join(FONT_DIR, font_name)


def put_text_on_image(img: Image.Image, text: str, font_name: str,
                      font_size: int, text_fill) -> None:
    """Draw ``text`` centered on ``img`` in place."""
    font = ImageFont.truetype(font_path(font_name), font_size)
    draw = ImageDraw.Draw(img)

    # Pillow >= 10 removed ``ImageDraw.textsize``; use the bounding box instead.
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    w, h = right - left, bottom - top
    center_w = (img.size[0] - w) // 2
    center_h = (img.size[1] - h) // 2
    draw.text((center_w, center_h), text, fill=text_fill, font=font)


def fill_image_with_rgb_noise(img: Image.Image) -> None:
    """Fill every pixel of ``img`` with a random RGB value in place."""
    pixels = img.load()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            pixels[x, y] = (randint(0, 255), randint(0, 255), randint(0, 255))


def cat_files(out_path: str, *in_files: str) -> None:
    """Concatenate ``in_files`` byte-for-byte into ``out_path``."""
    import shutil

    with open(out_path, "wb") as out_file:
        for in_path in in_files:
            with open(in_path, "rb") as in_file:
                shutil.copyfileobj(in_file, out_file)
