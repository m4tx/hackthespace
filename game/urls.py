"""stronghold URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
