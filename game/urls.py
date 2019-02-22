from django.urls import path, include

urlpatterns = [
    path('', include(('game.puzzles.urls', 'game'), namespace='puzzle')),
]
