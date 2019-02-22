from django.conf import settings

ORDER = settings.PUZZLE_ORDER


def get_first_puzzle():
    return ORDER[0]


def get_last_puzzle():
    return ORDER[-1]


def get_next_puzzle(puzzle: str):
    assert puzzle in ORDER, 'The puzzle was not found on the list'
    assert ORDER[-1] != puzzle, 'Given puzzle is the last one on the list'

    for index, val in enumerate(ORDER):
        if puzzle == val:
            return ORDER[index + 1]


def get_prev_puzzle(puzzle: str):
    assert puzzle in ORDER, 'The puzzle was not found on the list'
    assert ORDER[0] != puzzle, 'Given puzzle is the first one on the list'

    for index, val in enumerate(ORDER):
        if puzzle == val:
            return ORDER[index - 1]
