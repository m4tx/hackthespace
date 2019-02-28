from django.views.generic import TemplateView


class FinishPuzzleView(TemplateView):
    template_name = 'finish.html'
