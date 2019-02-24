from django.template import Library
from django.template.defaultfilters import stringfilter

register = Library()


def rot_char(char, offset):
    c = char.lower()
    if c.isalpha():
        o = ord(c) - ord('a') + offset
        o %= 26
        o += ord('a')
        c = chr(o)

        if char.isupper():
            c = c.upper()
    return c


def rot(value: str, offset):
    rv = ''

    for char in value:
        rv += rot_char(char, offset)

    return rv


@register.filter(name='rot', is_safe=True)
@stringfilter
def rot_filter(value, shift: int):
    """Applies a ROT encoding on the string."""
    return rot(value, shift)


