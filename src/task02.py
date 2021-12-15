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


def normalize_input(data):
    convert = lambda t: (t[0], int(t[1]))
    return list(map(convert, map(str.split, data)))


def solve_test(data):
    with suppress(NotImplementedError):
        print(f"Part 1: {calculate_position_part_one(data)}")

        print(f"Part 2: {calculate_position_part_two(data)}")


def solve_part_one(data):
    print(combine_position(calculate_position_part_one(data)))


def solve_part_two(data):
    print(combine_position(calculate_position_part_two(data)))


def main(test=False):
    global TEST
    TEST = test

    data = read_input()
    data = normalize_input(data)

    if TEST:
        solve_test(data)
    else:
        with suppress(NotImplementedError):
            solve_part_one(data)
            solve_part_two(data)


if __name__ == '__main__':
    main()


# LOGIC / SOLUTION

def calculate_position_part_one(data):
    x = 0
    depth = 0
    for direction, length in data:
        match direction:
            case 'forward':
                x += length
            case 'up':
                depth -= length
            case 'down':
                depth += length

    return x, depth


def combine_position(position):
    x, depth = position
    return x * depth


def calculate_position_part_two(data):
    x = 0
    depth = 0
    aim = 0
    for command, value in data:
        match command:
            case 'down':
                aim += value
            case 'up':
                aim -= value
            case 'forward':
                x += value
                depth += (value * aim)

    return x, depth
