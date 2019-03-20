from django.urls import path

from reverse.views import ReversePuzzleView

urlpatterns = [
    path('ayeayepatch/', ReversePuzzleView.as_view(), name='reverse'),
]
