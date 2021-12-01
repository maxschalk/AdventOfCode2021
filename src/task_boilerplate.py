from pathlib import Path

from PATHS import INPUT_DIR, TEST_INPUT_DIR

FILE_STEM = Path(__file__).stem

INPUT_FILE = INPUT_DIR.joinpath(f"{FILE_STEM}_input.txt")
TEST_INPUT_FILE = TEST_INPUT_DIR.joinpath(f"{FILE_STEM}_test_input.txt")


# BOILERPLATE

def read_input(test=False):
    path = TEST_INPUT_FILE if test else INPUT_FILE

    with open(path, "r") as file:
        lines = file.readlines()

    lines = list(map(str.strip, lines))

    return lines


def normalize_input(data):
    return data


def solve(data):
    raise NotImplementedError


def main(test=False):
    data = read_input(test=test)
    data = normalize_input(data)
    solve(data)


if __name__ == '__main__':
    main()


# LOGIC / SOLUTION

def _solve(data):
    raise NotImplementedError
