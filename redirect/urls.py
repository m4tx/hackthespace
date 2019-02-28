from django.urls import path

from redirect.views import RedirectPuzzleView, RedirectFailPuzzleView

urlpatterns = [
    path('wowsuchsecret/', RedirectPuzzleView.as_view(), name='redirect'),
    path('ysoslow/', RedirectFailPuzzleView.as_view(), name='redirect_fail'),
]
