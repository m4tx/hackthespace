from django.urls import path

from pages.views import PagesPuzzleView, PagesHiddenPuzzleView

urlpatterns = [
    path('pagelookup/', PagesPuzzleView.as_view(), name='pages'),
    path('weakgravity/', PagesHiddenPuzzleView.as_view(),
         name='pages_hidden'),
]
