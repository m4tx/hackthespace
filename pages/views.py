from django.db import OperationalError
from django.views.generic import ListView, TemplateView

from game.decorators import puzzle, hidden_puzzle, requires_email
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
            query = Puzzle.objects.raw(
                'SELECT * from pages_puzzle WHERE url = \'{}\''.format(
                    form.cleaned_data['query']))
            len(query)  # Force evaluate the query
            return query

        return Puzzle.objects.none()

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except OperationalError:
            self.object_list = []
            context = self.get_context_data()
            context['query_error'] = True
            return self.render_to_response(context)


@hidden_puzzle
@requires_email
class PagesHiddenPuzzleView(TemplateView):
    template_name = 'game/hidden_puzzle.html'
