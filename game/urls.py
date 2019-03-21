from django.urls import path

from game.views import EmailFormView

urlpatterns = [
    path('emailform/', EmailFormView.as_view(), name='email_form'),
]
