from django.conf import settings

ORDER = settings.PUZZLE_ORDER


def get_next_puzzle(puzzle: str):
    assert puzzle in ORDER
    assert ORDER[-1] != puzzle

    for index, val in enumerate(ORDER):
        if puzzle == val:
            return ORDER[index + 1]


def get_prev_puzzle(puzzle: str):
    assert puzzle in ORDER
    assert ORDER[0] != puzzle

    for index, val in enumerate(ORDER):
        if puzzle == val:
            return ORDER[index - 1]
