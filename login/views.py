from django import forms
from django.views.generic import FormView

from game.decorators import puzzle
from game.puzzle_order import get_next_puzzle_url


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)


@puzzle
class LoginPuzzleView(FormView):
    template_name = 'login/puzzle.html'
    form_class = LoginForm
    success_url = get_next_puzzle_url('login')

    username = 'Cannonbeam'
    password = 'starjammer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.username
        context['password'] = self.password
        return context

    def form_valid(self, form):
        if (form.cleaned_data['password'] != self.password or
                form.cleaned_data['username'] != self.username):
            form.add_error('password', 'The password you provided is invalid')
            return self.form_invalid(form)

        return super().form_valid(form)
