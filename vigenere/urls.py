from django.urls import path

from vigenere.views import VigenerePuzzleView

urlpatterns = [
    path('dramaticvinegar/', VigenerePuzzleView.as_view(), name='vigenere'),
]
