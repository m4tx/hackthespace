from django.views.generic import TemplateView

from game.decorators import puzzle


@puzzle
class RedirectPuzzleView(TemplateView):
    template_name = 'redirect.html'


class RedirectFailPuzzleView(TemplateView):
    template_name = 'redirect_fail.html'
