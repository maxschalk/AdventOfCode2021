import itertools
import re

from pathlib import Path
from contextlib import suppress

from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

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
    return [list(map(int, row)) for row in data]


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
    min_path = get_min_path(data)

    return sum(map(lambda t: data[t[1]][t[0]], min_path))


def get_min_path(data):
    grid = Grid(matrix=data)

    start = grid.node(0, 0)
    end = grid.node(len(data) - 1, len(data) - 1)

    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)

    path, runs = finder.find_path(start, end, grid)

    path.pop(0)

    return path


def _solve_part_two(data):
    matrix = extend_matrix(data)

    min_path = get_min_path(matrix)

    return sum(map(lambda t: matrix[t[1]][t[0]], min_path))


def extend_matrix(grid):
    extension = 5

    initial_rows = []

    for row in grid:
        initial_rows.append(list(itertools.chain.from_iterable(
            map(lambda x: (x + step - 1) % 9 + 1, row) for step in range(extension)
        )))

    new_grid = []

    for step in range(extension):
        for row in initial_rows:
            new_grid.append(list(map(lambda x: (x + step - 1) % 9 + 1, row)))

    return new_grid
