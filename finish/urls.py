from django.urls import path

from finish.views import FinishPuzzleView

urlpatterns = [
    path('quadrupedpirate/', FinishPuzzleView.as_view(), name='finish'),
]
