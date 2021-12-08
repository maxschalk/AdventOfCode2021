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
        solve(data)


if __name__ == '__main__':
    main()


def read_input(test: bool):
    path = TEST_INPUT_FILE if test else INPUT_FILE

    with open(path, "r") as file:
        content = file.read()

    return content.split('\n')


def parse_input(data, test):
    out = []

    pattern = re.compile(r"([a-z ]+)\|([a-z ]+)")

    for line in data:
        inputs, outputs = pattern.match(line).groups()

        out.append((inputs.strip().split(" "), outputs.strip().split(" ")))

    return out


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

"""
 aaaa 
b    c
b    c
 dddd 
e    f
e    f
 gggg
"""

DIGIT_MAP = {
    0: 'abcefg',
    1: 'cf',
    2: 'acdeg',
    3: 'acdfg',
    4: 'bcdf',
    5: 'abdfg',
    6: 'abdefg',
    7: 'acf',
    8: 'abcdefg',
    9: 'abcdfg'
}

LEN_DIGIT_MAP = {
    2: [1],
    3: [7],
    4: [4],
    5: [2, 3, 5],
    6: [0, 6, 9],
    7: [8]
}

"""
acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf

a: (c, f)
b: (c, f)

d: (a, c, f)    -> a

e: (b, d)
f: (b, d)

ab      -> 1            -> cf
dab     -> 7            -> acf
eafb    -> 4            -> bcdf
acedgfb -> 8            -> abcdefg
cdfbe   -> [2, 3, 5]    ->
gcdfa   -> [2, 3, 5]    ->
fbcad   -> [2, 3, 5]    ->
cefabd  -> [0, 6, 9]    ->
cdfgeb  -> [0, 6, 9]    ->
cagedb  -> [0, 6, 9]    ->

abcdefg -> deafgbc
"""


def _solve_part_one(data):
    targets = {2, 4, 3, 7}  # 1, 4, 7, 8
    count = 0

    for _, outputs in data:
        for output_len in map(len, outputs):
            count += output_len in targets

    return count


def _solve_part_two(data):
    return sum(decode_line(inputs, outputs) for inputs, outputs in data)


def decode_line(inputs, outputs):
    return 0
