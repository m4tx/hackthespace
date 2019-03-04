import pyminizip

import base64
import os
import tempfile
from PIL import Image
from django.conf import settings

from game.puzzles.order import get_next_puzzle_url
from game.utils.files import cat_files
from game.utils.images import put_text_on_image
from vendor.steglsb import LSBEncode

README_FILENAME = 'readme.txt'
INNER_ZIP_FILENAME = 'atme.zip'
PASSWORD_1 = 'This1sN0t'
PASSWORD_2 = '4nOrd1n@ryITFestival'
INNER_IMAGE_FILENAME = 'look.jpg'
OUTER_ZIP_FILENAME = 'outer.zip'
SECRET_IMAGE_NAME = 'secret.jpg'
COVER_IMAGE_NAME = 'cover.png'
OUTPUT_NAME = 'lookcloser.png'


class AssetGenerator:
    def __init__(self):
        self.puzzle_dir = os.path.dirname(os.path.abspath(__file__))
        self.assets_dir = os.path.join(self.puzzle_dir, 'assets')
        self.tmp_dir = None

        # Loaded from config
        self.font_name = None
        self.font_size = None
        self.text_fill = None
        self.bits_used = None

    def load_django_config(self):
        self.font_name = settings.PUZZLE_STEGO_MIX_FONT_NAME
        self.font_size = settings.PUZZLE_STEGO_MIX_FONT_SIZE
        self.text_fill = settings.PUZZLE_STEGO_MIX_TEXT_FILL
        self.bits_used = settings.PUZZLE_STEGO_MIX_BITS

    def __create_txt(self):
        with open(os.path.join(self.tmp_dir, README_FILENAME), 'w') as f:
            with open(os.path.join(self.assets_dir, README_FILENAME)) as in_f:
                readme_contents = in_f.read()

            f.write(readme_contents.format(get_next_puzzle_url('stego_mix')))

    def __create_inner_zip(self):
        readme_path = os.path.join(self.tmp_dir, README_FILENAME)
        inner_zip_path = os.path.join(self.tmp_dir, INNER_ZIP_FILENAME)
        password = PASSWORD_1 + PASSWORD_2

        pyminizip.compress(readme_path, '', inner_zip_path, password, 9)

    def __create_inner_image(self):
        pass_str = base64.b64encode(PASSWORD_2.encode('utf-8'))
        pass_path = os.path.join(self.tmp_dir, 'pass.txt')
        with open(pass_path, 'wb') as f:
            f.write(pass_str)

        inner_image_path = os.path.join(self.tmp_dir, INNER_IMAGE_FILENAME)
        inner_image_source_path = os.path.join(
            self.assets_dir, INNER_IMAGE_FILENAME)

        cat_files(inner_image_path, inner_image_source_path, pass_path)

    def __create_outer_zip(self):
        inner_image_path = os.path.join(self.tmp_dir, INNER_IMAGE_FILENAME)
        inner_zip_path = os.path.join(self.tmp_dir, INNER_ZIP_FILENAME)
        outer_zip_path = os.path.join(self.tmp_dir, OUTER_ZIP_FILENAME)

        pyminizip.compress_multiple(
            [inner_image_path, inner_zip_path],
            ['', ''],
            outer_zip_path, None, 9)

    def __create_secret_image(self):
        source_path = os.path.join(self.assets_dir, SECRET_IMAGE_NAME)
        dest_path = os.path.join(self.tmp_dir, SECRET_IMAGE_NAME)

        img = Image.open(source_path)
        put_text_on_image(img, PASSWORD_1, self.font_name, self.font_size,
                          self.text_fill)

        img.save(dest_path)

    def __encode_secret_image(self):
        cover_path = os.path.join(self.assets_dir, COVER_IMAGE_NAME)
        secret_path = os.path.join(self.tmp_dir, SECRET_IMAGE_NAME)
        dest_path = os.path.join(self.tmp_dir, OUTPUT_NAME)

        LSBEncode(cover_path, secret_path, self.bits_used, dest_path)

    def __generate_output(self):
        image_path = os.path.join(self.tmp_dir, OUTPUT_NAME)
        zip_path = os.path.join(self.tmp_dir, OUTER_ZIP_FILENAME)
        dest_dir = os.path.join(
            self.puzzle_dir, 'static', 'images', 'generated')
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, OUTPUT_NAME)

        cat_files(dest_path, image_path, zip_path)

    def generate(self):
        assert self.font_name is not None, 'Config was not loaded'

        with tempfile.TemporaryDirectory() as tmp_dir:
            self.tmp_dir = tmp_dir

            print('Creating TXT file')
            self.__create_txt()
            print('Generating inner ZIP file')
            self.__create_inner_zip()
            print('Generating inner image file')
            self.__create_inner_image()
            print('Generating outer ZIP file')
            self.__create_outer_zip()
            print('Generating secret image file')
            self.__create_secret_image()
            print('Encoding the secret image file')
            self.__encode_secret_image()
            print('Generating the output file')
            self.__generate_output()
