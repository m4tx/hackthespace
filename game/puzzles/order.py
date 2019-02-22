from django.conf import settings
from django.urls import reverse

ORDER = settings.PUZZLE_ORDER


# Puzzle names
def get_first_puzzle() -> str:
    return ORDER[0]


def get_last_puzzle() -> str:
    return ORDER[-1]


def get_next_puzzle(puzzle: str) -> str:
    assert puzzle in ORDER, 'The puzzle was not found on the list'
    assert ORDER[-1] != puzzle, 'Given puzzle is the last one on the list'

    for index, val in enumerate(ORDER):
        if puzzle == val:
            return ORDER[index + 1]


def get_prev_puzzle(puzzle: str) -> str:
    assert puzzle in ORDER, 'The puzzle was not found on the list'
    assert ORDER[0] != puzzle, 'Given puzzle is the first one on the list'

    for index, val in enumerate(ORDER):
        if puzzle == val:
            return ORDER[index - 1]


# Puzzle URLs
def get_first_puzzle_url() -> str:
    return reverse('puzzle:' + get_first_puzzle())


def get_last_puzzle_url() -> str:
    return reverse('puzzle:' + get_last_puzzle())


def get_next_puzzle_url(puzzle: str) -> str:
    return reverse('puzzle:' + get_next_puzzle(puzzle))


def get_prev_puzzle_url(puzzle: str) -> str:
    return reverse('puzzle:' + get_prev_puzzle(puzzle))
