from django.urls import path

from audio_spectrum.views import AudioSpectrumPuzzleView

urlpatterns = [
    path('spacemetal/', AudioSpectrumPuzzleView.as_view(),
         name='audio_spectrum'),
]
