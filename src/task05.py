import re

from pathlib import Path
from contextlib import suppress

from PATHS import TASK_INPUT_DIR, TEST_INPUT_DIR

FILE_STEM = Path(__file__).stem

INPUT_FILE = TASK_INPUT_DIR.joinpath(f"{FILE_STEM}_input.txt")
TEST_INPUT_FILE = TEST_INPUT_DIR.joinpath(f"{FILE_STEM}_test_input.txt")

TEST = False


# BOILERPLATE

def read_input():
    path = TEST_INPUT_FILE if TEST else INPUT_FILE

    with open(path, "r") as file:
        lines = file.readlines()

    lines = list(map(str.strip, lines))

    return lines


def parse_input(data, test):
    out = []

    pattern = re.compile(r"\d+")

    for line in data:
        start_x, start_y, end_x, end_y = map(int, pattern.findall(line))
        out.append(((start_x, start_y), (end_x, end_y)))

    return out


def solve_test(data):
    with suppress(NotImplementedError):
        print(f"Part 1 - {_solve_part_one(data)}")

        print(f"Part 2 - {_solve_part_two(data)}")


def solve(data):
    with suppress(NotImplementedError):
        solve_part_one(data)
        solve_part_two(data)


def solve_part_one(data):
    print(_solve_part_one(data))


def solve_part_two(data):
    print(_solve_part_two(data))


def main(test=False):
    global TEST
    TEST = test

    data = read_input()
    data = parse_input(data, test)

    if TEST:
        solve_test(data)
    else:
        solve(data)


if __name__ == '__main__':
    main()


# LOGIC / SOLUTION

def _solve_part_one(data):
    lines = list(filter(is_one_dimensional, data))

    return _solve(lines)


def _solve_part_two(data):
    return _solve(data)


def _solve(coordinates):
    width = max(map(lambda t: max(t[0][0], t[1][0]), coordinates)) + 1
    height = max(map(lambda t:  max(t[0][1], t[1][1]), coordinates)) + 1

    grid = [[0] * width for _ in range(height)]

    _mark_coordinates(grid, coordinates)

    result = 0

    for row in grid:
        # print(str.join('', map(str, row)).replace('0', '.'))
        result += len(tuple(filter(lambda x: x >= 2, row)))

    return result


def is_one_dimensional(coordinates):
    (start_x, start_y), (end_x, end_y) = coordinates

    return start_x == end_x or start_y == end_y


def _mark_coordinates(grid, lines):
    for coordinates in lines:
        for x, y in line_coordinates(coordinates):
            grid[y][x] += 1


def line_coordinates(coordinates):
    (start_x, start_y), (end_x, end_y) = coordinates

    length = max(abs(start_x - end_x), abs(start_y - end_y)) + 1

    xs = (start_x,) * length if start_x == end_x else list(range(*_range_args(start_x, end_x)))
    ys = (start_y,) * length if start_y == end_y else list(range(*_range_args(start_y, end_y)))

    return zip(xs, ys)


def _range_args(start, end):
    if start <= end:
        return start, end + 1, 1
    else:
        return start, end - 1, -1

