from django.views.generic import FormView

from game.forms import EmailForm
from game.models import Player
from game.puzzle_order import get_puzzle_url


class EmailFormView(FormView):
    template_name = 'game/email_form.html'
    form_class = EmailForm

    def form_valid(self, form):
        player = Player.get_player(self.request)
        player.email = form.cleaned_data['email']
        player.save()

        return super().form_valid(form)

    def get_initial(self):
        player = Player.get_player(self.request)
        return {
            'email': player.email,
        }

    def get_success_url(self):
        return get_puzzle_url(Player.get_player(self.request).last_puzzle)
