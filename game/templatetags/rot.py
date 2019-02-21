from django.template import Library
from django.template.defaultfilters import stringfilter

register = Library()


def rot(value: str, offset):
    rv = ''

    for char in value:
        c = char.lower()

        if ord('a') <= ord(c) <= ord('z'):
            o = ord(c) - ord('a') + offset
            o %= 26
            o += ord('a')
            c = chr(o)

            if char.isupper():
                c = c.upper()

        rv += c

    return rv


@register.filter(is_safe=True)
@stringfilter
def rot19(value):
    """Applies a rot19 encoding on the string."""
    return rot(value, 19)
