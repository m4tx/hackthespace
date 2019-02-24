from django.urls import path

from game.puzzles.image.puzzle import ImagePuzzleView
from game.puzzles.redirect.puzzle import RedirectFailPuzzleView
from game.puzzles.redirect.puzzle import RedirectPuzzleView
from game.puzzles.rot13.puzzle import Rot13PuzzleView
from game.puzzles.terminal.puzzle import TerminalPuzzleView
from game.puzzles.login.puzzle import LoginPuzzleView
from game.puzzles.finish.puzzle import FinishPuzzleView
from game.puzzles.audio_spectrum.puzzle import AudioSpectrumPuzzleView
from game.puzzles.vigenere.puzzle import VigenerePuzzleView

urlpatterns = [
    path('', Rot13PuzzleView.as_view(), name='rot13'),

    path('toomuchwant/', ImagePuzzleView.as_view(), name='image'),
    path('h4x.sh/', TerminalPuzzleView.as_view(), name='terminal'),

    path('wowsuchsecret/', RedirectPuzzleView.as_view(), name='redirect'),
    path('ysoslow/', RedirectFailPuzzleView.as_view(), name='redirect_fail'),

    path('login/', LoginPuzzleView.as_view(), name='login'),
    path('spacemetal/', AudioSpectrumPuzzleView.as_view(),
         name='audio_spectrum'),
    path('vinegar/', VigenerePuzzleView.as_view(), name='vigenere'),

    path('finish/', FinishPuzzleView.as_view(), name='finish'),
]
