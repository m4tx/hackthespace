import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.urls import reverse

from game.puzzles.image.generate_image import put_text_on_image
from game.puzzles.order import get_next_puzzle


class Command(BaseCommand):
    help = 'Generate image file for "image" puzzle'

    def handle(self, *args, **kwargs):
        app_root = os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))))
        puzzle_root = os.path.join(app_root, 'puzzles', 'image')
        source_path = os.path.join(puzzle_root, 'img', 'source.png')
        font_path = os.path.join(puzzle_root,
                                 'fonts', 'Roboto', 'Roboto-Black.ttf')

        dest_dir = os.path.join(app_root, 'static', 'images', 'generated')
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, 'lookatme.png')

        put_text_on_image(
            source_path, dest_path,
            reverse('puzzle:' + get_next_puzzle('image')),
            font_path, settings.PUZZLE_IMAGE_FONT_SIZE)
