from django.views.generic import TemplateView


class SkyPuzzleView(TemplateView):
    template_name = 'puzzles/sky.html'
