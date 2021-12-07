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
        from timeit import timeit
        print(timeit(lambda: solve(data), number=1))
        # solve(data)


# (328, 328187)
# (464, 91257582)

if __name__ == '__main__':
    main()


def read_input(test: bool):
    path = TEST_INPUT_FILE if test else INPUT_FILE

    with open(path, "r") as file:
        content = file.read()

    return content.split('\n')


def parse_input(data, test):
    pattern = re.compile(r",")
    first_line, *_ = data
    return list(map(int, pattern.split(first_line)))


def solve_test(data):
    with suppress(NotImplementedError):
        print(f"Part 1 - {_solve_part_one(data)}")

        print('-' * 30)

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
    return min(((i, distance_cumul(data, i)) for i in range(min(data), max(data) + 1)),
               key=lambda t: t[1])


def distance_cumul(values, target):
    return sum(map(lambda val: abs(val - target), values))


def _solve_part_two(data):
    return min(((i, fuel_cumul(data, i)) for i in range(min(data), max(data) + 1)),
               key=lambda t: t[1])


def fuel_cumul(values, target):
    return sum(map(lambda val: _fuel_consumption(abs(val - target)), values))


FUEL_CONSUMPTION = dict()


def _fuel_consumption(distance):
    # if distance not in FUEL_CONSUMPTION:
    #     FUEL_CONSUMPTION[distance] = sum(range(distance, -1, -1))
    #
    # return FUEL_CONSUMPTION[distance]

    return sum(range(distance, -1, -1))
