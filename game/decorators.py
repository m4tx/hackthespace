from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from typing import Type

from game.models import SolvedPuzzle, Player, SolvedHiddenPuzzle
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


def requires_email(cls: Type[View]):
    orig_dispatch = cls.dispatch

    def new_dispatch(self, request, *args, **kwargs):
        response = orig_dispatch(self, request, *args, **kwargs)

        player = Player.get_player(request)

        # Only allow proceeding to the current puzzle if the user provided
        # their email address
        if not player.email:
            request.session['email_next'] = request.path
            return redirect(reverse('email_form'))

        return response

    cls.dispatch = new_dispatch
    return cls


def hidden_puzzle(cls: Type[View]):
    orig_dispatch = cls.dispatch

    cls.puzzle_name = cls.__module__.split('.')[0]

    def new_dispatch(self, request, *args, **kwargs):
        response = orig_dispatch(self, request, *args, **kwargs)

        player = Player.get_player(request)

        if not SolvedPuzzle.objects.filter(
                player=player, puzzle=cls.puzzle_name).exists():
            raise Http404

        if not SolvedHiddenPuzzle.objects.filter(
                player=player, puzzle=cls.puzzle_name).exists():
            SolvedHiddenPuzzle.objects.create(
                player=player, puzzle=cls.puzzle_name,
                timestamp=timezone.now())

        return response

    cls.dispatch = new_dispatch
    return cls
