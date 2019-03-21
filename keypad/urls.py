from django.urls import path

from keypad.views import KeypadPuzzleView

urlpatterns = [
    path('keypad/', KeypadPuzzleView.as_view(), name='keypad'),
]
