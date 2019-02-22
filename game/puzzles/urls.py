from django.urls import path

from game.puzzles.image.puzzle import ImagePuzzleView
from game.puzzles.redirect.puzzle import RedirectFailPuzzleView
from game.puzzles.redirect.puzzle import RedirectPuzzleView
from game.puzzles.rot13.puzzle import Rot13PuzzleView
from game.puzzles.terminal.puzzle import TerminalPuzzleView

urlpatterns = [
    path('', Rot13PuzzleView.as_view(), name='rot13'),
    path('toomuchwant/', ImagePuzzleView.as_view(), name='image'),
    path('h4x.sh/', TerminalPuzzleView.as_view(), name='terminal'),

    path('redirect/', RedirectPuzzleView.as_view(), name='redirect'),
    path('ysoslow/', RedirectFailPuzzleView.as_view(), name='redirect_fail'),

]
