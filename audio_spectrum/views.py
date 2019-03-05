from django.views.generic import TemplateView

from game.decorators import puzzle


@puzzle
class AudioSpectrumPuzzleView(TemplateView):
    template_name = 'audio_spectrum.html'
