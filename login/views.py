from django import forms
from django.views.generic import FormView

from game.puzzles.order import get_next_puzzle_url


class LoginForm(forms.Form):
    password = forms.CharField(max_length=50)


class LoginPuzzleView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = get_next_puzzle_url('login')

    password = 'neverhood'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['password'] = self.password
        return context

    def form_valid(self, form):
        if form.cleaned_data['password'] != self.password:
            form.add_error('password', 'The password you provided is invalid')
            return self.form_invalid(form)

        return super().form_valid(form)
