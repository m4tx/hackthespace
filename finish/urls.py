from django.urls import path

from finish.views import FinishPuzzleView

urlpatterns = [
    path('quadruped_pirate/', FinishPuzzleView.as_view(), name='finish'),
]
