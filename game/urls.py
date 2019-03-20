from django.urls import path

from game.views import EmailFormView

urlpatterns = [
    path('email_form/', EmailFormView.as_view(), name='email_form'),
]
