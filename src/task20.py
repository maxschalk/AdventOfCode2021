import collections
import re

from collections import deque
from pathlib import Path
from contextlib import suppress

from PATHS import TEST_INPUT_DIR, TASK_INPUT_DIR

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
    enhancement_algo, sep_line, *image = data

    return enhancement_algo, list(image)


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

LIGHT_PIXEL = '#'
DARK_PIXEL = '.'

DIRECTIONS = (
    (-1, -1), (0, -1), (1, -1),
    (-1, 0), (0, 0), (1, 0),
    (-1, 1), (0, 1), (1, 1),
)


def _solve_part_one(data):
    return _solve(data, 2)


def _solve_part_two(data):
    return _solve(data, 50)


def _solve(data, steps):
    lookup, image = data

    lookup = lookup.replace('.', '0').replace('#', '1')

    width = len(image[0]) + 2 * steps
    height = len(image) + 2 * steps

    image = coordinate_map(image, extend_by_steps=steps)

    for step in range(steps):
        image = enhance_image(lookup, image, width, height, step)

    return sum(image.values())


def pixel_to_int(pixel):
    return 1 if pixel == LIGHT_PIXEL else 0


def coordinate_map(image, extend_by_steps):
    result = dict()

    for y, row in enumerate([*([DARK_PIXEL * len(image[0])] * extend_by_steps),
                             *image,
                             *([DARK_PIXEL * len(image[0])] * extend_by_steps)]):

        for x, value in enumerate([*(DARK_PIXEL * extend_by_steps), *row, *(DARK_PIXEL * extend_by_steps)]):
            result[(x, y)] = pixel_to_int(value)

    return result


def enhance_image(lookup, image, width, height, step):
    result = dict()

    for x in range(width):
        for y in range(height):
            lookup_index = str.join('', map(str, neighbors(lookup=lookup, coordinates=image, x=x, y=y, step=step)))
            lookup_index = int(lookup_index, 2)

            result[(x, y)] = int(lookup[lookup_index])

    return result


def neighbors(lookup, coordinates, x, y, step):
    for dx, dy in DIRECTIONS:
        yield coordinates.get((x + dx, y + dy), outside_pixel(lookup=lookup, step=step))


def outside_pixel(lookup, step):
    if step % 2 == 0 and lookup[-1] == '0':
        return 0

    if step % 2 == 1 and lookup[0] == '1':
        return 1

    return 0
