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
    return list(map(lambda s: list(map(int, s)), data))


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

def _solve_part_one(data):
    return sum(1 + data[y][x] for x, y in all_low_points(data))


def _solve_part_two(data):
    raise NotImplementedError


def all_low_points(data):
    result = []

    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

    max_y = len(data) - 1
    max_x = len(data[0]) - 1

    for y, row in enumerate(data):
        for x, value in enumerate(row):
            lowest = True

            for dir in directions:
                dy, dx = dir
                new_x = x + dx
                new_y = y + dy

                if new_x < 0 or new_x > max_x or new_y < 0 or new_y > max_y:
                    continue

                if value >= data[new_y][new_x]:
                    lowest = False
                    break

            if lowest:
                result.append((x, y))

    return result
