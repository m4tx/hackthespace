import pyminizip
from time import sleep

import base64
import os
import tempfile

from game.puzzles.order import get_next_puzzle_url
from game.utils.files import cat_files

README_FILENAME = 'readme.txt'
INNER_ZIP_FILENAME = 'atme.zip'
PASSWORD_1 = 'This1sN0t'
PASSWORD_2 = '4nOrd1n@ryITFestival'
INNER_IMAGE_FILENAME = 'look.jpg'
OUTER_ZIP_FILENAME = 'outer.zip'


class AssetGenerator:
    def __init__(self):
        self.puzzle_dir = os.path.dirname(os.path.abspath(__file__))
        self.assets_dir = os.path.join(self.puzzle_dir, 'assets')
        self.tmp_dir = None

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
        img = Image.open(source_path).convert('RGBA')
        txt = Image.new('RGBA', img.size, (0, 0, 0, 0))

        put_text_on_image(txt, text, font_name, font_size, fill)
        combined = Image.alpha_composite(img, txt)

        combined.save(dest_path)

    def __encode_secret_image(self):
        pass

    def __generate_output(self):
        pass

    def generate(self):
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
            sleep(100)
