from django.urls import path

from reverse.views import ReversePuzzleView

urlpatterns = [
    path('program/', ReversePuzzleView.as_view(), name='reverse'),
]
