import os

from PIL import Image, ImageFont, ImageDraw
from random import randint


def put_text_on_image(img: Image, text: str,
                      font_name: str, font_size: int, text_fill):
    """
    Puts given text at the center of the image passed.

    :param img: image to put the text on
    :param text: text to put
    :param font_name: name of the font file (relative to the fonts/ directory)
        to use
    :param font_size: desired text size
    :param text_fill: text color, e.g. as 4-tuple (0, 0, 0, 255)
    """
    font_path = os.path.join(os.path.dirname(__file__), 'fonts', font_name)
    font = ImageFont.truetype(font_path, font_size)
    d = ImageDraw.Draw(img)

    w, h = d.textsize(text, font=font)
    center_w = (img.size[0] - w) // 2
    center_h = (img.size[1] - h) // 2
    d.text((center_w, center_h), text, fill=text_fill, font=font)


def fill_image_with_rgb_noise(img):
    pixels = img.load()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            pixels[x, y] = (randint(0, 255), randint(0, 255), randint(0, 255))
