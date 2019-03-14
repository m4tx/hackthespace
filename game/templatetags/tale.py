from django.template import Library

from game.templatetags.puzzles import get_current_puzzle

register = Library()


@register.inclusion_tag('tale.html', takes_context=True)
def tale(context):
    return {
        'filename': '{}/tale.txt'.format(get_current_puzzle(context)),
    }
