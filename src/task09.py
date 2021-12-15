from functools import reduce
from operator import mul
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

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def _solve_part_one(data):
    return sum(1 + data[y][x] for x, y in all_low_points(data))


def _solve_part_two(data):
    low_points = all_low_points(data)

    basins = basins_from_low_points(data, low_points)

    basins = sorted(basins, key=len, reverse=True)

    return reduce(mul, map(len, basins[:3]))


def _solve_part_two_oneliner(data):
    return reduce(mul, map(len, sorted(basins_from_low_points(data, all_low_points(data)), key=len, reverse=True)[:3]))


def all_low_points(data):
    result = []

    max_y = len(data) - 1
    max_x = len(data[0]) - 1

    for y, row in enumerate(data):
        for x, value in enumerate(row):
            lowest = True

            for dx, dy in DIRECTIONS:
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


def basins_from_low_points(grid, low_points):
    basins = []

    max_x = len(grid[0]) - 1
    max_y = len(grid) - 1

    for lp in low_points:
        basin = {lp}

        _basin(grid, max_x, max_y, lp, basin)

        basins.append(basin)

    return basins


def _basin(grid, max_x, max_y, start, visited):
    x, y = start
    for dx, dy in DIRECTIONS:
        new_x = x + dx
        new_y = y + dy

        if new_x < 0 or new_x > max_x or new_y < 0 or new_y > max_y:
            continue

        if (new_x, new_y) in visited:
            continue

        value = grid[y][x]
        neighbor = grid[new_y][new_x]

        if value < neighbor < 9:
            visited.add((new_x, new_y))
            _basin(grid, max_x, max_y, (new_x, new_y), visited)
