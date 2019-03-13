from django.template import Library

register = Library()


@register.inclusion_tag('tale.html')
def tale(filename):
    return {
        'filename': filename,
    }
