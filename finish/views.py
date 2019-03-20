from django.views.generic import TemplateView

from game.decorators import puzzle, requires_email


@puzzle
@requires_email
class FinishPuzzleView(TemplateView):
    template_name = 'finish/puzzle.html'
