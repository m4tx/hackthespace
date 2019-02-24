from django.views.generic import TemplateView


class VigenerePuzzleView(TemplateView):
    template_name = 'puzzles/vigenere.html'
