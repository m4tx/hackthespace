from django.core.management.base import BaseCommand

from stego_mix.asset_generator import AssetGenerator


class Command(BaseCommand):
    help = 'Generate audio file for "audio spectrum" puzzle'

    def handle(self, *args, **kwargs):
        AssetGenerator().generate()
