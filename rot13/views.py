from django.urls import reverse, get_resolver
from django.views.generic import TemplateView


class Rot13PuzzleView(TemplateView):
    template_name = 'rot13.html'
