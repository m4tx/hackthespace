from django.views.generic import TemplateView

from game.decorators import puzzle


@puzzle
class RedirectPuzzleView(TemplateView):
    template_name = 'redirect/puzzle.html'


class RedirectFailPuzzleView(TemplateView):
    template_name = 'redirect/fail.html'
