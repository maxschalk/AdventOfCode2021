import re

from pathlib import Path
from contextlib import suppress

from PATHS import INPUT_DIR, TEST_INPUT_DIR

FILE_STEM = Path(__file__).stem

INPUT_FILE = INPUT_DIR.joinpath(f"{FILE_STEM}_input.txt")
TEST_INPUT_FILE = TEST_INPUT_DIR.joinpath(f"{FILE_STEM}_test_input.txt")


# BOILERPLATE


def main(test=False):
    data = read_input(test)
    data = parse_input(data, test)

    if test:
        solve_test(data)
    else:
        solve(data)


if __name__ == '__main__':
    main()


def read_input(test: bool):
    path = TEST_INPUT_FILE if test else INPUT_FILE

    with open(path, "r") as file:
        content = file.read()

    return content.split('\n')


def parse_input(data, test):
    return data


def solve_test(data):
    with suppress(NotImplementedError):
        print(f"Part 1 - {_solve_part_one(data)}")

        print('-' * 15)

        print(f"Part 2 - {_solve_part_two(data)}")

def solve(data):
    with suppress(NotImplementedError):
        solve_part_one(data)
        solve_part_two(data)


def solve_part_one(data):
    print(_solve_part_one(data))


def solve_part_two(data):
    print(_solve_part_two(data))


# SOLUTION

parentheses = ["()", "[]", "{}", "<>"]

PAIRS = {tuple(p) for p in parentheses}

OPENS = set(map(lambda t: t[0], parentheses))
CLOSES = set(map(lambda t: t[1], parentheses))

OPEN_TO_CLOSE = {t[0]: t[1] for t in parentheses}
CLOSE_TO_OPEN = {t[1]: t[0] for t in parentheses}

ILLEGAL_POINTS = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

AUTOCOMPLETE_POINTS = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}


def _solve_part_one(data):
    points = 0

    for line in data:
        opened = []

        for c in line:
            if c in OPENS:
                opened.append(c)
                continue

            if CLOSE_TO_OPEN[c] == opened[-1]:
                opened.pop()
            else:
                points += ILLEGAL_POINTS[c]
                opened.pop()
                break

    return points


def _solve_part_two(data):
    line_points = []

    for line in data:
        opened = []

        for c in line:
            if c in OPENS:
                opened.append(c)
                continue

            if CLOSE_TO_OPEN[c] == opened[-1]:
                opened.pop()
            else:
                break
        else:
            points = 0
            for open in reversed(opened):
                points *= 5
                points += AUTOCOMPLETE_POINTS[OPEN_TO_CLOSE[open]]

            line_points.append(points)

    return sorted(line_points)[len(line_points)//2]
