from django.views.generic import TemplateView


class AudioSpectrumPuzzleView(TemplateView):
    template_name = 'puzzles/audio_spectrum.html'
