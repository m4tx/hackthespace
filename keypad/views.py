from django.views.generic import TemplateView


class KeypadPuzzleView(TemplateView):
    template_name = 'keypad/puzzle.html'
