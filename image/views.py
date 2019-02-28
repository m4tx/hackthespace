from django.views.generic import TemplateView


class ImagePuzzleView(TemplateView):
    template_name = 'image.html'
