from django.urls import path

from pages.views import PagesPuzzleView

urlpatterns = [
    path('pagelookup/', PagesPuzzleView.as_view(), name='pages'),
]
