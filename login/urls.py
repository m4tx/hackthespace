from django.urls import path

from login.views import LoginPuzzleView

urlpatterns = [
    path('goawayfromhere/', LoginPuzzleView.as_view(), name='login'),
]
