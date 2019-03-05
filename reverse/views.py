from django.views.generic import TemplateView

from game.puzzles.order import get_next_puzzle_url

KEY = [
    0x9f, 0xd0, 0x27, 0x60, 0xab, 0x4c, 0xbe, 0xcf, 0x43, 0xe7, 0xd0, 0xe0,
    0x1c, 0x75, 0x87, 0x56, 0xc8, 0x3c
]


class ReversePuzzleView(TemplateView):
    template_name = 'reverse.html'

    def get_context_data(self, **kwargs):
        context = super(ReversePuzzleView, self).get_context_data(**kwargs)

        context['key'] = KEY
        context['encoded_url'] = self.encode_url(
            get_next_puzzle_url('reverse'), KEY)

        return context

    def encode_url(self, s, key):
        print(len(s))
        print(len(key))
        return [ord(x) ^ key[i] for i, x in enumerate(reversed(s))]
