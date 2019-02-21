from django.views.generic import TemplateView


class ImagePuzzleView(TemplateView):
    template_name = 'puzzles/image.html'
