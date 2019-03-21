from django.views.generic import TemplateView

from game.decorators import puzzle, hidden_puzzle, requires_email


@puzzle
class TerminalPuzzleView(TemplateView):
    template_name = 'terminal/puzzle.html'


@hidden_puzzle
@requires_email
class TerminalHiddenPuzzleView(TemplateView):
    template_name = 'terminal/hidden_puzzle.html'
