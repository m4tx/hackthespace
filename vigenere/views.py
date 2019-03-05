from django.views.generic import TemplateView

from game.decorators import puzzle


@puzzle
class VigenerePuzzleView(TemplateView):
    template_name = 'vigenere.html'
