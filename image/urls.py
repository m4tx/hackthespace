from django.urls import path

from image.views import ImagePuzzleView

urlpatterns = [
    path('lookclosely/', ImagePuzzleView.as_view(), name='image'),
]
