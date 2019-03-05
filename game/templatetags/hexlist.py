from django.template import Library
from django.template.defaultfilters import stringfilter
from typing import List

register = Library()


@register.filter(is_safe=True)
def hexlist(value: List[int]):
    return ', '.join('0x{:02x}'.format(x) for x in value)
