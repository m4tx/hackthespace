#!/usr/bin/env python3
"""One-off generator for the "stego mix" puzzle asset (lookcloser.jpg).

Builds a JPEG/ZIP polyglot whose appended archive contains:
  * ``look.png`` with a secret image (carrying PASSWORD_1) LSB-embedded in it,
  * ``at.jpg`` with base64(PASSWORD_2) appended,
  * a ZipCrypto-encrypted ``me.zip`` holding the readme with the next URL.

Ported out of the old Django management command ``generate_stego_mix_assets``
(see git history before commit f4ab363).

This is NOT part of the Rust build -- faithful reproduction depends on
``pyminizip`` (traditional ZipCrypto archives), which has no clean pure-Rust
equivalent, so this stays as a manual Python tool. Run it when the asset needs
regenerating, then copy ``output/lookcloser.jpg`` over
``static/static/images/generated/lookcloser.jpg``.

Requires: Pillow, pyminizip. See requirements.txt.

Usage:
    cd tools && python generate_stego_mix.py
"""
import base64
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pyminizip  # noqa: E402
from PIL import Image  # noqa: E402

from common import cat_files, put_text_on_image  # noqa: E402
from vendor.steglsb import LSBEncode  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(HERE, "assets", "stego")
OUTPUT_DIR = os.path.join(HERE, "output")

# The URL of the puzzle that follows "stego_mix" (reverse) in the Rust router
# (src/main.rs).
NEXT_PUZZLE_URL = "/ayeayepatch/"

# Values previously kept in the Django settings (PUZZLE_STEGO_MIX_*).
FONT_NAME = "Roboto/Roboto-Black.ttf"
FONT_SIZE = 150
TEXT_FILL = (0, 0, 0, 255)
BITS_USED = 3

PASSWORD_1 = "This1sN0t"
PASSWORD_2 = "4nOrd1n@ryITFestival"

README_FILENAME = "readme.txt"
INNER_ZIP_FILENAME = "me.zip"
INNER_IMAGE_FILENAME_1 = "look.png"
INNER_IMAGE_FILENAME_2 = "at.jpg"
OUTER_ZIP_FILENAME = "outer.zip"
SECRET_IMAGE_NAME = "secret.jpg"
COVER_IMAGE_NAME = "cover.jpg"
OUTPUT_NAME = "lookcloser.jpg"


def create_txt(tmp_dir):
    with open(os.path.join(ASSETS_DIR, README_FILENAME)) as in_f:
        contents = in_f.read()
    with open(os.path.join(tmp_dir, README_FILENAME), "w") as f:
        f.write(contents.format(NEXT_PUZZLE_URL))


def create_inner_zip(tmp_dir):
    readme_path = os.path.join(tmp_dir, README_FILENAME)
    inner_zip_path = os.path.join(tmp_dir, INNER_ZIP_FILENAME)
    pyminizip.compress(readme_path, "", inner_zip_path,
                       PASSWORD_1 + PASSWORD_2, 9)


def create_secret_image(tmp_dir):
    img = Image.open(os.path.join(ASSETS_DIR, SECRET_IMAGE_NAME))
    put_text_on_image(img, PASSWORD_1, FONT_NAME, FONT_SIZE, TEXT_FILL)
    img.save(os.path.join(tmp_dir, SECRET_IMAGE_NAME))


def create_inner_image_1(tmp_dir):
    LSBEncode(
        os.path.join(ASSETS_DIR, INNER_IMAGE_FILENAME_1),
        os.path.join(tmp_dir, SECRET_IMAGE_NAME),
        BITS_USED,
        os.path.join(tmp_dir, INNER_IMAGE_FILENAME_1),
    )


def create_inner_image_2(tmp_dir):
    pass_path = os.path.join(tmp_dir, "pass.txt")
    with open(pass_path, "wb") as f:
        f.write(base64.b64encode(PASSWORD_2.encode("utf-8")))
    cat_files(
        os.path.join(tmp_dir, INNER_IMAGE_FILENAME_2),
        os.path.join(ASSETS_DIR, INNER_IMAGE_FILENAME_2),
        pass_path,
    )


def create_outer_zip(tmp_dir):
    pyminizip.compress_multiple(
        [os.path.join(tmp_dir, INNER_IMAGE_FILENAME_1),
         os.path.join(tmp_dir, INNER_IMAGE_FILENAME_2),
         os.path.join(tmp_dir, INNER_ZIP_FILENAME)],
        ["", "", ""],
        os.path.join(tmp_dir, OUTER_ZIP_FILENAME), None, 9)


def generate_output(tmp_dir):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    cat_files(
        os.path.join(OUTPUT_DIR, OUTPUT_NAME),
        os.path.join(ASSETS_DIR, COVER_IMAGE_NAME),
        os.path.join(tmp_dir, OUTER_ZIP_FILENAME),
    )


def main():
    with tempfile.TemporaryDirectory() as tmp_dir:
        print("Creating TXT file")
        create_txt(tmp_dir)
        print("Generating inner ZIP file")
        create_inner_zip(tmp_dir)
        print("Generating secret image file")
        create_secret_image(tmp_dir)
        print("Generating first inner image file")
        create_inner_image_1(tmp_dir)
        print("Generating second inner image file")
        create_inner_image_2(tmp_dir)
        print("Generating outer ZIP file")
        create_outer_zip(tmp_dir)
        print("Generating the output file")
        generate_output(tmp_dir)
        print("Done! Output in", OUTPUT_DIR)


if __name__ == "__main__":
    main()
