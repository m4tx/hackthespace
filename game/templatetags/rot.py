from django.template import Library
from django.template.defaultfilters import stringfilter

register = Library()


def rot_char(char: str, offset: int):
    c = char.lower()

    if c.isalpha():
        o = ord(c) - ord('a') + offset
        o %= 26
        o += ord('a')
        c = chr(o)

        if char.isupper():
            c = c.upper()

    return c


@register.filter(name='rot')
@stringfilter
def rot(value: str, offset: int):
    """Encrypt given string using ROT cipher."""
    rv = ''

    for char in value:
        rv += rot_char(char, offset)

    return rv


@register.filter
def vigenere(value: str, key: str):
    """Encrypt given string using Vigenère cipher."""
    key = key.lower()
    string = ''
    index = 0

    for c in value:
        if c.isalpha():
            string += rot_char(c, ord(key[index]) - ord('a'))
            index += 1
            index %= len(key)
        else:
            string += c

    return string
