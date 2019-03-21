from django.urls import path

from keypad.views import KeypadPuzzleView

urlpatterns = [
    path('doorkeypad/', KeypadPuzzleView.as_view(), name='keypad'),
]
