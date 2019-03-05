from django.core.management import call_command

from django.core.management.base import BaseCommand

COMMANDS = [
    'generate_image_assets',
    'generate_audio_spectrum_assets',
    'generate_stego_mix_assets',
]


class Command(BaseCommand):
    help = 'Generate puzzle assets'

    def handle(self, *args, **options):
        for i, cmd in enumerate(COMMANDS):
            self.stdout.write(self.style.SUCCESS(
                'Running command {}/{}: {}'.format(i + 1, len(COMMANDS), cmd)))
            call_command(cmd)
