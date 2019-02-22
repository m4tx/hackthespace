import hashlib
from django import template

register = template.Library()


@register.simple_tag
def md5(string: str):
    return hashlib.md5(string.encode('utf-8')).hexdigest()
