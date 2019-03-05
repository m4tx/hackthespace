import random
import string
from django.http import Http404
from django.shortcuts import redirect
from django.utils import timezone
from django.views import View
from typing import Type

from game.models import Player, SolvedPuzzle
from game.puzzles.order import (
    get_first_puzzle, puzzle_less, get_next_puzzle, get_puzzle_url,
    get_last_puzzle)

SID_CHARS = string.ascii_uppercase + string.ascii_lowercase + string.digits


def generate_sid(length=20, chars=SID_CHARS):
    return ''.join(random.choice(chars) for _ in range(length))


def get_player(request):
    if ('sid' in request.COOKIES and
            Player.objects.filter(session_id=request.COOKIES['sid']).exists()):
        sid = request.COOKIES['sid']
        player = Player.objects.get(session_id=sid)
    else:
        sid = generate_sid()
        player = Player.objects.create(session_id=sid)
        SolvedPuzzle.objects.create(
            player=player, puzzle=get_first_puzzle(),
            timestamp=timezone.now())
    return player, sid


def puzzle(cls: Type[View]):
    orig_dispatch = cls.dispatch

    cls.puzzle_name = cls.__module__.split('.')[0]

    def new_dispatch(self, request, *args, **kwargs):
        response = orig_dispatch(self, request, *args, **kwargs)

        player, sid = get_player(request)

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
            'sid', sid, expires=timezone.now() + timezone.timedelta(days=365))

        return response

    cls.dispatch = new_dispatch
    return cls
