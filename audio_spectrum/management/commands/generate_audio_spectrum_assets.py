import os
from django.conf import settings
from django.core.management.base import BaseCommand

from audio_spectrum.asset_generator import hide_text_in_audio
from game.puzzles.order import get_next_puzzle_url


class Command(BaseCommand):
    help = 'Generate audio file for "audio spectrum" puzzle'

    def handle(self, *args, **kwargs):
        app_root = os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))))
        source_path = os.path.join(app_root, 'audio', 'deadlyfox.ogg')

        dest_dir = os.path.join(app_root, 'static', 'audio', 'generated')
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, 'deadlyfox')

        hide_text_in_audio(
            input_path=source_path,
            out_path=dest_path,
            text=str(get_next_puzzle_url('audio_spectrum')),
            font_name=settings.PUZZLE_AUDIO_SPECTRUM_FONT_NAME,
            font_size=settings.PUZZLE_AUDIO_SPECTRUM_FONT_SIZE,
            min_freq=settings.PUZZLE_AUDIO_SPECTRUM_MIN_FREQ,
            max_freq=settings.PUZZLE_AUDIO_SPECTRUM_MAX_FREQ,
            pixels_per_second=settings.PUZZLE_AUDIO_SPECTRUM_PPS,
            audio_position=settings.PUZZLE_AUDIO_SPECTRUM_AUDIO_POS,
            audio_gain=settings.PUZZLE_AUDIO_SPECTRUM_AUDIO_GAIN,
            audio_tags=settings.PUZZLE_AUDIO_SPECTRUM_TAGS)
