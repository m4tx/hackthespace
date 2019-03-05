from django.core.management.base import BaseCommand

from stego_mix.asset_generator import AssetGenerator


class Command(BaseCommand):
    help = 'Generate audio file for "stego mix" puzzle'

    def handle(self, *args, **kwargs):
        generator = AssetGenerator()
        generator.load_django_config()
        generator.generate()
