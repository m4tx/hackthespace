from django.views.generic import ListView

from game.decorators import puzzle
from pages.forms import SearchForm
from pages.models import Puzzle


@puzzle
class PagesPuzzleView(ListView):
    template_name = 'pages/puzzle.html'
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
