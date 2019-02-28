from django.urls import path

from sky.views import SkyPuzzleView

urlpatterns = [
    path('toomuchwant/', SkyPuzzleView.as_view(), name='sky'),
]
