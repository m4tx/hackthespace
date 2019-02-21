from django.views.generic import TemplateView


class TerminalPuzzleView(TemplateView):
    template_name = 'puzzles/terminal.html'
