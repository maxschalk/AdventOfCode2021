import re

from collections import Counter
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
    pattern = re.compile(r",")

    result = pattern.split(data[0])

    return list(map(int, result))


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

REPRODUCTION_CYCLE = 6

FIRST_CYCLE_DELAY = 2

FIRST_REPRODUCTION_CYCLE = REPRODUCTION_CYCLE + FIRST_CYCLE_DELAY


def _solve_part_one(data):
    return fish_after_days(data, 80)


def _solve_part_two(data):
    return fish_after_days(data, 256)


def fish_after_days(fish_ages, days):
    ages = [0] * (FIRST_REPRODUCTION_CYCLE + 1)

    for age, count in Counter(fish_ages).items():
        ages[age] = count

    for _ in range(days):
        ages = ages[1:] + ages[:1]
        ages[REPRODUCTION_CYCLE] += ages[FIRST_REPRODUCTION_CYCLE]

    return sum(ages)
