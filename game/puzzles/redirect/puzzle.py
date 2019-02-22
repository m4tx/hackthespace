from django.views.generic import TemplateView


class RedirectPuzzleView(TemplateView):
    template_name = 'puzzles/redirect.html'


class RedirectFailPuzzleView(TemplateView):
    template_name = 'puzzles/redirect_fail.html'
