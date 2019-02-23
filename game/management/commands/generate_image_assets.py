import os
from django.conf import settings
from django.core.management.base import BaseCommand

from game.puzzles.image.asset_generator import generate_image
from game.puzzles.order import get_next_puzzle_url


class Command(BaseCommand):
    help = 'Generate image file for "image" puzzle'

    def handle(self, *args, **kwargs):
        app_root = os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))))
        puzzle_root = os.path.join(app_root, 'puzzles', 'image')
        source_path = os.path.join(puzzle_root, 'img', 'source.png')

        dest_dir = os.path.join(app_root, 'static', 'images', 'generated')
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, 'lookatme.png')

        generate_image(source_path, dest_path,
                       str(get_next_puzzle_url('image')),
                       settings.PUZZLE_IMAGE_FONT_NAME,
                       settings.PUZZLE_IMAGE_FONT_SIZE,
                       settings.PUZZLE_IMAGE_FILL)
