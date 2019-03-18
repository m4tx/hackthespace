import random
from django import template
from django.utils.safestring import mark_safe

from game.puzzle_order import get_next_puzzle_url

register = template.Library()

CHARS = '.,✦*˚'
SPACE = '\u2003'
ITEM_NUM = 100


def rand_gray():
    color = random.randint(100, 255)
    return '{0:02x}'.format(color) * 3


@register.simple_tag
def generate_sky():
    s = ''
    chosen = random.randint(0, ITEM_NUM - 1)

    for i in range(ITEM_NUM):
        s += '<span style="color: #{}">'.format(rand_gray())
        if i == chosen:
            s += '<a href="' + str(get_next_puzzle_url('sky')) + '">'
            s += '★'
            s += '</a>'
        else:
            s += random.choice(CHARS)
        s += '</span>'

        for _ in range(random.randint(10, 24)):
            s += SPACE
            if random.randint(0, 1) == 1:
                s += ' '

    return mark_safe(s)
