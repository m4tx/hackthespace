from django.urls import path

from stego_mix.views import StegoMixPuzzleView

urlpatterns = [
    path('lookcloser/', StegoMixPuzzleView.as_view(), name='stego_mix'),
]
