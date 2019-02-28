from django.urls import path

from terminal.views import TerminalPuzzleView

urlpatterns = [
    path('h4x.sh/', TerminalPuzzleView.as_view(), name='terminal'),
]
