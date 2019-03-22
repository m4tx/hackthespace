from django.db import OperationalError
from django.views.generic import ListView, TemplateView

from game.decorators import puzzle, hidden_puzzle, requires_email
from pages.forms import SearchForm
from pages.models import Puzzle

SQL_KEYWORDS = ['add', 'alter', 'asc', 'backup', 'between', 'case', 'check',
                'column', 'constraint', 'create', 'database', 'default',
                'delete', 'desc', 'distinct', 'drop', 'exec', 'exists',
                'foreign', 'from', 'full', 'group', 'having', 'index', 'inner',
                'insert', 'join', 'left', 'like', 'limit', 'order', 'outer',
                'primary', 'procedure', 'right', 'rownum', 'select', 'set',
                'table', 'top', 'truncate', 'union', 'unique', 'update',
                'values', 'view', 'pg_']


@puzzle
class PagesPuzzleView(ListView):
    template_name = 'pages/puzzle.html'
    form_class = SearchForm
    model = Puzzle

    db_name = 'sql_injection'

    def get_queryset(self):
        form = self.form_class(self.request.GET)

        if form.is_valid():
            q = form.cleaned_data['query'].lower()

            if any(keyword in q for keyword in SQL_KEYWORDS):
                return Puzzle.objects.none()

            query = Puzzle.objects.raw(
                'SELECT * from pages_puzzle WHERE url = \'{}\''.format(
                    q))
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
