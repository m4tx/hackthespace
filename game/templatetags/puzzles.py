from django import template
from django.template import RequestContext
from django.urls import resolve

from game.puzzle_order import (
    get_next_puzzle, get_prev_puzzle, get_first_puzzle, get_last_puzzle,
    get_first_puzzle_url, get_last_puzzle_url, get_next_puzzle_url,
    get_prev_puzzle_url, get_puzzle_url)

register = template.Library()


def get_current_puzzle(context: RequestContext):
    return resolve(context.request.path).app_name


# Puzzle names
@register.simple_tag(takes_context=True)
def current_puzzle(context):
    return get_current_puzzle(context)


@register.simple_tag
def first_puzzle():
    return get_first_puzzle()


@register.simple_tag
def last_puzzle():
    return get_last_puzzle()


@register.simple_tag(takes_context=True)
def next_puzzle(context: RequestContext):
    return get_next_puzzle(get_current_puzzle(context))


@register.simple_tag(takes_context=True)
def prev_puzzle(context: RequestContext):
    return get_prev_puzzle(get_current_puzzle(context))


# Puzzle URLs
@register.simple_tag(takes_context=True)
def current_puzzle_url(context):
    return get_puzzle_url(current_puzzle(context))


@register.simple_tag
def first_puzzle_url():
    return get_first_puzzle_url()


@register.simple_tag
def last_puzzle_url():
    return get_last_puzzle_url()


@register.simple_tag(takes_context=True)
def next_puzzle_url(context: RequestContext):
    return get_next_puzzle_url(get_current_puzzle(context))


@register.simple_tag(takes_context=True)
def prev_puzzle_url(context: RequestContext):
    return get_prev_puzzle_url(get_current_puzzle(context))
