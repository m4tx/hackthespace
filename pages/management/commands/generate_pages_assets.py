import random
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from game.puzzle_order import get_puzzle_url
from pages.models import Puzzle

MIN_TIME_DIFF = timezone.timedelta(days=3)
MAX_TIME_DIFF_SEC = 3 * 7 * 24 * 60 * 60  # 3 weeks


class Command(BaseCommand):
    help = 'Generate DB entries for "pages" puzzle'

    def __put_puzzle_data(self):
        Puzzle.objects.all().delete()

        end = False
        for id, puzzle in enumerate(settings.PUZZLE_ORDER, 1):
            Puzzle(pk=id, url=get_puzzle_url(puzzle), name=puzzle,
                   date=self.__random_date()).save()

            if end:
                break
            elif puzzle == 'pages':
                end = True
                # End after putting one puzzle coming after "pages"

    @staticmethod
    def __random_date():
        diff_sec = random.randint(0, MAX_TIME_DIFF_SEC)
        return (timezone.now() -
                MIN_TIME_DIFF -
                timezone.timedelta(seconds=diff_sec))

    def handle(self, *args, **kwargs):
        self.__put_puzzle_data()
