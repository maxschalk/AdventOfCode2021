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

    if test:
        solve_test(lambda: parse_input(data, test))
    else:
        solve(lambda: parse_input(data, test))


if __name__ == '__main__':
    main()


def read_input(test: bool):
    path = TEST_INPUT_FILE if test else INPUT_FILE

    with open(path, "r") as file:
        content = file.read()

    return content.split('\n')


def parse_input(data, test):
    out = ([], [])

    coord_pattern = re.compile(r"(\d+),(\d+)")
    fold_pattern = re.compile(r"fold along ([a-z])=(\d+)")

    sep_line_reached = False

    for line in data:
        if not sep_line_reached and not line.strip():
            sep_line_reached = True
            continue

        if not sep_line_reached:
            x, y = coord_pattern.match(line).groups()
            out[0].append({'x': int(x), 'y': int(y)})
        else:
            axis, location = fold_pattern.match(line).groups()
            out[1].append((axis, int(location)))

    return out


def solve_test(data):
    with suppress(NotImplementedError):
        print(f"Part 1 - {_solve_part_one(data())}")

        print('-' * 15)

        print(f"Part 2 - {_solve_part_two(data())}")


def solve(data):
    with suppress(NotImplementedError):
        solve_part_one(data())
        solve_part_two(data())


def solve_part_one(data):
    print(_solve_part_one(data))


def solve_part_two(data):
    print(_solve_part_two(data))


# SOLUTION

def _solve_part_one(data):
    dot_coordinates, fold_instructions = data

    for fold_instruction in fold_instructions[:1]:
        fold(dot_coordinates, fold_instruction)

    return len(set(map(tuple, map(dict.values, dot_coordinates))))


def fold(dot_coordinates, fold_instruction):
    axis, fold_location = fold_instruction

    for dot_coordinate in dot_coordinates:
        value = dot_coordinate[axis]

        if fold_location >= value:
            continue

        new_value = value - 2 * (value - fold_location)

        dot_coordinate[axis] = new_value


EMPTY = ' '
FILLED = '\u25A0'


def _solve_part_two(data):
    dot_coordinates, fold_instructions = data

    for fold_instruction in fold_instructions:
        fold(dot_coordinates, fold_instruction)

    final_coords = set(map(tuple, map(dict.values, dot_coordinates)))

    max_x = max(map(lambda t: t[0], final_coords))
    max_y = max(map(lambda t: t[1], final_coords))

    result = [list(EMPTY * (max_x + 1)) for _ in range(max_y + 1)]

    for y, row in enumerate(result):
        for x, _ in enumerate(row):
            if (x, y) in final_coords:
                result[y][x] = FILLED

    pretty_print(result)


def pretty_print(data):

    transposed = list(zip(*data))

    spaced = []

    for row in transposed:
        if all(map(lambda c: c == EMPTY, row)):
            for _ in range(3):
                spaced.append(row)

        spaced.append(row)

    data = list(map(list, zip(*spaced)))

    for y, row in enumerate(data):
        for x, value in enumerate(row):
            if value == EMPTY:
                continue

            top = y > 0 and data[y-1][x] != EMPTY
            bottom = y < len(data) - 1 and data[y+1][x] != EMPTY

            left = x > 0 and data[y][x-1] != EMPTY
            right = x < len(data[0]) - 1 and data[y][x+1] != EMPTY

            top_left = y > 0 and x > 0 and data[y-1][x-1] != EMPTY
            bottom_left = y < len(data) - 1 and x > 0 and data[y+1][x-1] != EMPTY
            bottom_right = y < len(data) - 1 and x < len(data[0]) - 1 and data[y+1][x+1] != EMPTY
            top_right = y > 0 and x < len(data[0]) - 1 and data[y-1][x+1] != EMPTY

            if top and bottom:
                row[x] = '|'
            elif left and right:
                row[x] = '-'
            elif top or bottom:
                row[x] = '|'
            elif left or right:
                row[x] = '-'
            elif top_left or bottom_right:
                row[x] = '\\'
            elif bottom_left or top_right:
                row[x] = '/'

    print("\u001b[40;1m", end="")
    print("\u001b[33;1m", end="")
    print("\u001b[1m", end="")

    print("\n".join(map(lambda r: f"{str.join('', r)}", data)))

    print("\u001b[0m")
