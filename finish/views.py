from django.views.generic import TemplateView

from game.decorators import puzzle


@puzzle
class FinishPuzzleView(TemplateView):
    template_name = 'finish/puzzle.html'
