from django.conf import settings
from django.db import models
from django.utils.functional import cached_property

PUZZLES = ((name, name) for name in settings.PUZZLE_ORDER)


class Player(models.Model):
    session_id = models.CharField(max_length=20, db_index=True, unique=True)
    email = models.EmailField(max_length=100, blank=True)

    @cached_property
    def last_puzzle(self) -> str:
        return self.solvedpuzzle_set.order_by('-timestamp').first().puzzle

    def __str__(self):
        s = self.session_id
        if self.email:
            s += ' ({})'.format(self.email)
        return s


class SolvedPuzzle(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    puzzle = models.CharField(max_length=40, choices=PUZZLES)
    timestamp = models.DateTimeField()

    class Meta:
        index_together = [
            ('player', 'puzzle')
        ]
