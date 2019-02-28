from django.views.generic import TemplateView


class RedirectPuzzleView(TemplateView):
    template_name = 'redirect.html'


class RedirectFailPuzzleView(TemplateView):
    template_name = 'redirect_fail.html'
