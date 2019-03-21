from django.urls import path

from terminal.views import TerminalPuzzleView, TerminalHiddenPuzzleView

urlpatterns = [
    path('h4x.sh/', TerminalPuzzleView.as_view(), name='terminal'),
    path('wow.sh/', TerminalHiddenPuzzleView.as_view(),
         name='terminal_hidden'),
]
