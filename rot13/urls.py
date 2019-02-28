from django.urls import path

from rot13.views import Rot13PuzzleView

urlpatterns = [
    path('', Rot13PuzzleView.as_view(), name='rot13'),
]
