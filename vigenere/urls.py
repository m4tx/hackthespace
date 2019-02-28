from django.urls import path

from vigenere.views import VigenerePuzzleView

urlpatterns = [
    path('vinegar/', VigenerePuzzleView.as_view(), name='vigenere'),
]
