from django.views.generic import FormView

from game.puzzle_order import get_next_puzzle_url
from keypad.forms import KeypadForm


class KeypadPuzzleView(FormView):
    template_name = 'keypad/puzzle.html'
    form_class = KeypadForm

    def get_success_url(self):
        return get_next_puzzle_url('keypad')
