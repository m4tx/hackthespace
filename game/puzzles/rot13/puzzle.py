from django.views.generic import TemplateView


class Rot13PuzzleView(TemplateView):
    template_name = 'puzzles/rot13.html'
