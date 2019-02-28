from django import forms
from django.views.generic import ListView

from pages.models import Puzzle


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)


class PagesPuzzleView(ListView):
    template_name = 'pages.html'
    form_class = SearchForm
    model = Puzzle

    db_name = 'sql_injection'

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            return Puzzle.objects.raw(
                'SELECT * from pages_puzzle WHERE url = \'{}\''.format(
                    form.cleaned_data['query']))

        return Puzzle.objects.none()
