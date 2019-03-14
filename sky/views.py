from django.views.generic import TemplateView

from game.decorators import puzzle


@puzzle
class SkyPuzzleView(TemplateView):
    template_name = 'sky/puzzle.html'
