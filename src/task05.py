from pathlib import Path
from contextlib import suppress

from PATHS import INPUT_DIR, TEST_INPUT_DIR

FILE_STEM = Path(__file__).stem

INPUT_FILE = INPUT_DIR.joinpath(f"{FILE_STEM}_input.txt")
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
    return data


def solve_test(data):
    with suppress(NotImplementedError):
        for line in data:
            print(f"Part 1: {line}: {_solve_part_one(line)}")

        for line in data:
            print(f"Part 2: {line}: {_solve_part_two(line)}")


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
    raise NotImplementedError


def _solve_part_two(data):
    raise NotImplementedError
