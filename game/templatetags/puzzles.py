from django import template
from django.template import RequestContext
from django.urls import reverse, resolve

from game.puzzles.order import (
    get_next_puzzle, get_prev_puzzle, get_first_puzzle, get_last_puzzle)

register = template.Library()


def __get_current_puzzle(context: RequestContext):
    return resolve(context.request.path).url_name


# Puzzle names
@register.simple_tag
def first_puzzle():
    return get_first_puzzle()


@register.simple_tag
def last_puzzle():
    return get_last_puzzle()


@register.simple_tag(takes_context=True)
def next_puzzle(context: RequestContext):
    return get_next_puzzle(__get_current_puzzle(context))


@register.simple_tag(takes_context=True)
def prev_puzzle(context: RequestContext):
    return get_prev_puzzle(__get_current_puzzle(context))


# Puzzle URLs
@register.simple_tag
def first_puzzle_url():
    return reverse('puzzle:' + get_first_puzzle())


@register.simple_tag
def last_puzzle_url():
    return reverse('puzzle:' + get_last_puzzle())


@register.simple_tag(takes_context=True)
def next_puzzle_url(context: RequestContext):
    return reverse('puzzle:' + get_next_puzzle(__get_current_puzzle(context)))


@register.simple_tag(takes_context=True)
def prev_puzzle_url(context: RequestContext):
    return reverse('puzzle:' + get_prev_puzzle(__get_current_puzzle(context)))
