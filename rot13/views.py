from django.views.generic import TemplateView

from game.decorators import puzzle


@puzzle
class Rot13PuzzleView(TemplateView):
    template_name = 'rot13/puzzle.html'
