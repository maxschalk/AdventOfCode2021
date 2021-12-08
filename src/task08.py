import re

from collections import defaultdict
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

def _solve_part_one(data):
    targets = {2, 4, 3, 7}  # 1, 4, 7, 8
    count = 0

    for _, outputs in data:
        for output_len in map(len, outputs):
            count += output_len in targets

    return count


def _solve_part_two(data):
    return sum(decode_line(inputs, outputs) for inputs, outputs in data)


"""
acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf

ab -> cf

dab -> acf
d -> a

eafb -> bcdf
ef -> bd

cdfbe -> [acdeg, acdfg, abdfg]
cdfbe -> abdfg
bcdef -> abdfg
b -> f
a -> c
c -> g
ef -> bd

gcdfa -> [acdeg, acdfg, abdfg]
acdfg -> [acdeg, acdfg]
f -> d
e -> b
g -> e

fbcad -> [acdeg, acdfg, abdfg]
fbcad -> acdfg


ab      -> 1            -> cf
dab     -> 7            -> acf
eafb    -> 4            -> bcdf
acedgfb -> 8            -> abcdefg
cdfbe   -> [2, 3, 5]    -> [acdeg, acdfg, abdfg]
gcdfa   -> [2, 3, 5]    -> [acdeg, acdfg, abdfg]
fbcad   -> [2, 3, 5]    -> [acdeg, acdfg, abdfg]
cefabd  -> [0, 6, 9]    -> [abcefg, abdefg, abcdfg]
cdfgeb  -> [0, 6, 9]    -> [abcefg, abdefg, abcdfg]
cagedb  -> [0, 6, 9]    -> [abcefg, abdefg, abcdfg]

abcdefg -> deafgbc
"""

"""
     aaaa 
    b    c
    b    c
     dddd 
    e    f
    e    f
     gggg

DIGIT_TO_SIGNAL_MAP = {
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

LEN_TO_DIGIT_MAP = {
    2: [1],
    3: [7],
    4: [4],
    5: [2, 3, 5],
    6: [0, 6, 9],
    7: [8]
}
"""

DIGIT_TO_SIGNAL_MAP = {
    0: frozenset('abcefg'),
    1: frozenset('cf'),
    2: frozenset('acdeg'),
    3: frozenset('acdfg'),
    4: frozenset('bcdf'),
    5: frozenset('abdfg'),
    6: frozenset('abdefg'),
    7: frozenset('acf'),
    8: frozenset('abcdefg'),
    9: frozenset('abcdfg')
}

SIGNAL_TO_DIGIT_MAP = {signals: digit for digit, signals in DIGIT_TO_SIGNAL_MAP.items()}

DIGIT_TO_LEN_MAP = {digit: len(signals) for digit, signals in DIGIT_TO_SIGNAL_MAP.items()}

LEN_TO_DIGIT_MAP = defaultdict(list)

for digit, len_signals in DIGIT_TO_LEN_MAP.items():
    LEN_TO_DIGIT_MAP[len_signals].append(digit)

UNIQUE_LENGTHS = {2, 4, 3, 7}

# be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe

"""
1: 'cf'
4: 'bcdf'
7: 'acf'
8: 'abcdefg'
"""


def decode_line(inputs, outputs):
    solution = dict()

    for signals in inputs:
        possible_digits = LEN_TO_DIGIT_MAP[len(signals)]
        if len(possible_digits) == 1:
            digit, *_ = possible_digits

            solution[signals] = ''.join(DIGIT_TO_SIGNAL_MAP[digit])
        else:
            solution[signals] = [''.join(DIGIT_TO_SIGNAL_MAP[digit]) for digit in possible_digits]

    # print("\n".join(map(str, sorted(solution.items(), key=lambda t: len(t[0])))))

    while not complete_solution(solution):
        resolve_solution(solution)

    translation = translate_outputs(outputs, solution)

    result = ''.join(str(SIGNAL_TO_DIGIT_MAP[frozenset(signal)]) for signal in translation)

    return int(result)


def complete_solution(solution):
    return all(map(bool, (solution.get(char) for char in 'abcdefg')))


def resolve_solution(solutions):
    initial = list(solutions.items())

    for signal_in, signal_possibilites in initial:
        if isinstance(signal_possibilites, list):
            continue

        to_add = [(signal_in, signal_possibilites)]
        to_del = []

        for signal_in2, signal_possibilites2 in solutions.items():
            if signal_in == signal_in2:
                continue

            if isinstance(signal_possibilites2, str):
                if set(signal_in) < set(signal_in2):
                    new_key = ''.join(set(signal_in2) - set(signal_in))
                    new_val = ''.join(set(signal_possibilites2) - set(signal_possibilites))

                    to_add.append((new_key, new_val))
                    to_del.append(signal_in2)
            else:
                if set(signal_in) < set(signal_in2):
                    new_key = ''.join(set(signal_in2) - set(signal_in))

                    new_val = []

                    for possibility in signal_possibilites2:
                        if not set(signal_possibilites) < set(possibility):
                            continue

                        new_val.append(''.join(set(possibility) - set(signal_possibilites)))

                    if len(new_val) == 1:
                        new_val, *_ = new_val

                    to_add.append((new_key, new_val))
                    to_del.append(signal_in2)

        for key in to_del:
            del solutions[key]

        for key, val in to_add:
            solutions[key] = val


def translate_outputs(outputs, solution):
    return [str.join('', (solution[char] for char in output)) for output in outputs]
