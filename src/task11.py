import re

from pathlib import Path
from contextlib import suppress

from PATHS import TASK_INPUT_DIR, TEST_INPUT_DIR

FILE_STEM = Path(__file__).stem

INPUT_FILE = TASK_INPUT_DIR.joinpath(f"{FILE_STEM}_input.txt")
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
    return list(map(lambda row: list(map(int, row)), data))


def solve_test(data):
    with suppress(NotImplementedError):
        data_copy = list(map(lambda row: row[:], data))
        print(f"Part 1 - {_solve_part_one(data_copy)}")

        print('-' * 15)

        data_copy = list(map(lambda row: row[:], data))
        print(f"Part 2 - {_solve_part_two(data_copy)}")


def solve(data):
    with suppress(NotImplementedError):
        data_copy = list(map(lambda row: row[:], data))
        solve_part_one(data_copy)

        data_copy = list(map(lambda row: row[:], data))
        solve_part_two(data_copy)


def solve_part_one(data):
    print(_solve_part_one(data))


def solve_part_two(data):
    print(_solve_part_two(data))


# SOLUTION

STEPS = 100

DIRECTIONS = (
    (-1, -1), (0, -1), (1, -1),
    (-1, 0), (1, 0),
    (-1, 1), (0, 1), (1, 1)
)


def _solve_part_one(data):
    max_x = len(data[0]) - 1
    max_y = len(data) - 1

    flashes = 0

    for _ in range(STEPS):
        for y, row in enumerate(data):
            for x, value in enumerate(row):
                increment_rec(data, (x, y), (max_x, max_y))

        for y, row in enumerate(data):
            for x, value in enumerate(row):
                if value > 9:
                    flashes += 1
                    row[x] = 0

    return flashes


def increment_2d(grid, value):
    return list(map(lambda row: increment(row, value), grid))


def increment(row, value):
    return list(map(lambda x: x + value, row))


def increment_rec(grid, pos, max_pos):
    x, y = pos
    max_x, max_y = max_pos

    if x < 0 or x > max_x or y < 0 or y > max_y:
        return

    if grid[y][x] > 9:
        return

    grid[y][x] += 1

    if grid[y][x] <= 9:
        return

    for dx, dy in DIRECTIONS:
        new_x = x + dx
        new_y = y + dy

        increment_rec(grid, (new_x, new_y), max_pos)


def _solve_part_two(data):
    max_x = len(data[0]) - 1
    max_y = len(data) - 1

    steps = 0

    while True:

        for y, row in enumerate(data):
            for x, value in enumerate(row):
                increment_rec(data, (x, y), (max_x, max_y))

        steps += 1

        if all(map(lambda row: all(map(lambda x: x > 9, row)), data)):
            return steps

        for y, row in enumerate(data):
            for x, value in enumerate(row):
                if value > 9:
                    row[x] = 0
