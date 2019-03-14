from django.views.generic import TemplateView

from game.decorators import puzzle


@puzzle
class StegoMixPuzzleView(TemplateView):
    template_name = 'stego_mix/puzzle.html'
