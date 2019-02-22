from django.urls import path

from game.puzzles.terminal.puzzle import TerminalPuzzleView
from game.puzzles.image.puzzle import ImagePuzzleView
from game.puzzles.rot13.puzzle import Rot13PuzzleView
from game.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('rot13/', Rot13PuzzleView.as_view(), name='rot13'),
    path('toomuchwant/', ImagePuzzleView.as_view(), name='image'),
    path('h4x.sh/', TerminalPuzzleView.as_view(), name='terminal'),
]
