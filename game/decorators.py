from django.http import Http404
from django.utils import timezone
from django.views import View
from typing import Type

from game.models import SolvedPuzzle, Player
from game.puzzle_order import puzzle_less, get_next_puzzle, get_last_puzzle


def puzzle(cls: Type[View]):
    orig_dispatch = cls.dispatch

    cls.puzzle_name = cls.__module__.split('.')[0]

    def new_dispatch(self, request, *args, **kwargs):
        response = orig_dispatch(self, request, *args, **kwargs)

        player = Player.get_player(request)

        # Only allow proceeding to the next puzzle
        if player.last_puzzle != get_last_puzzle():
            next_puzzle = get_next_puzzle(player.last_puzzle)

            if next_puzzle == cls.puzzle_name:
                SolvedPuzzle.objects.create(
                    player=player, puzzle=next_puzzle,
                    timestamp=timezone.now())
            elif puzzle_less(player.last_puzzle, cls.puzzle_name):
                raise Http404

        response.set_cookie(
            'sid', player.session_id,
            expires=timezone.now() + timezone.timedelta(days=365))

        return response

    cls.dispatch = new_dispatch
    return cls
