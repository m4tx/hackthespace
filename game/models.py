import random
import string
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property

from game.puzzle_order import get_first_puzzle

PUZZLES = ((name, name) for name in settings.PUZZLE_ORDER)

SID_CHARS = string.ascii_uppercase + string.ascii_lowercase + string.digits


class Player(models.Model):
    session_id = models.CharField(max_length=20, db_index=True, unique=True)
    email = models.EmailField(max_length=100, blank=True)

    @cached_property
    def last_puzzle(self) -> str:
        return self.solvedpuzzle_set.order_by('-timestamp').first().puzzle

    @staticmethod
    def generate_sid(length=20, chars=SID_CHARS):
        return ''.join(random.choice(chars) for _ in range(length))

    @staticmethod
    def get_player(request) -> 'Player':
        if ('sid' in request.COOKIES and
                Player.objects.filter(
                    session_id=request.COOKIES['sid']).exists()):
            sid = request.COOKIES['sid']
            player = Player.objects.get(session_id=sid)
        else:
            sid = Player.generate_sid()
            player = Player.objects.create(session_id=sid)
            SolvedPuzzle.objects.create(
                player=player, puzzle=get_first_puzzle(),
                timestamp=timezone.now())

        return player

    def __str__(self):
        s = self.session_id
        if self.email:
            s += ' ({})'.format(self.email)
        return s


class AbstractSolvedPuzzle(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    puzzle = models.CharField(max_length=40, choices=PUZZLES)
    timestamp = models.DateTimeField()

    class Meta:
        index_together = [
            ('player', 'puzzle')
        ]
        abstract = True


class SolvedPuzzle(AbstractSolvedPuzzle):
    pass


class SolvedHiddenPuzzle(AbstractSolvedPuzzle):
    pass
