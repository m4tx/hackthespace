from django.views.generic import TemplateView


class FinishPuzzleView(TemplateView):
    template_name = 'puzzles/finish.html'
