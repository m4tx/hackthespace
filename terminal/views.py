from django.views.generic import TemplateView

from game.decorators import puzzle


@puzzle
class TerminalPuzzleView(TemplateView):
    template_name = 'terminal.html'
