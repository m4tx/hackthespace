import random
from django import template
from django.utils.safestring import mark_safe

from game.puzzles.order import get_next_puzzle_url

register = template.Library()

CHARS = '.,✦*˚'
SPACE = '\u2003'
ITEM_NUM = 100


@register.simple_tag
def generate_sky():
    s = ''
    chosen = random.randint(0, ITEM_NUM - 1)

    for i in range(ITEM_NUM):
        if i == chosen:
            s += '<a href="' + str(get_next_puzzle_url('sky')) + '">'
            s += '★'
            s += '</a>'
        else:
            s += random.choice(CHARS)

        for _ in range(random.randint(10, 24)):
            s += SPACE
            if random.randint(0, 1) == 1:
                s += ' '

    return mark_safe(s)
