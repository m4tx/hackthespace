from django.views.generic import FormView

from game.decorators import puzzle
from game.puzzle_order import get_next_puzzle_url
from keypad.forms import KeypadForm


@puzzle
class KeypadPuzzleView(FormView):
    template_name = 'keypad/puzzle.html'
    form_class = KeypadForm

    def get_success_url(self):
        return get_next_puzzle_url(KeypadPuzzleView.puzzle_name)
