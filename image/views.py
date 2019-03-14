from django.views.generic import TemplateView

from game.decorators import puzzle


@puzzle
class ImagePuzzleView(TemplateView):
    template_name = 'image/puzzle.html'
