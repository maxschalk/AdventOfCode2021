import collections
import re

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
    template, sep_line, *insertions = data

    out = []

    pattern = re.compile(r"([A-Z]+) -> ([A-Z]+)")

    for line in insertions:
        start, end = pattern.match(line).groups()

        out.append((start, end))

    return template, out


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
    return _solve(data, 10)


def _solve_part_two(data):
    return _solve(data, 40)


def _solve(data, steps):
    template, insertions = data

    insertion_map = {tuple(start): end for start, end in insertions}

    pair_counts = get_pair_counter(template)

    for _ in range(steps):
        pair_counts = insertion_step(pair_counts, insertion_map)

    counts = get_single_counts(pair_counts, template, as_sorted_list=True)

    min_elem = counts[0]
    max_elem = counts[-1]

    return max_elem[1] - min_elem[1]


def get_pair_counter(polymer):
    elements = collections.defaultdict(int)

    for index in range(len(polymer) - 1):
        char1 = polymer[index]
        char2 = polymer[index + 1]

        elements[(char1, char2)] += 1

    return elements


def insertion_step(pair_counts, insertion_map):
    new_pair_counts = collections.defaultdict(int)

    for key, value in pair_counts.items():
        char1, char2 = key
        insertion_char = insertion_map[key]

        new_pair_counts[(char1, insertion_char)] += value
        new_pair_counts[(insertion_char, char2)] += value

    return new_pair_counts


def get_single_counts(pair_counts, original_polymer, as_sorted_list=False):
    counts = collections.defaultdict(int)

    for (char1, char2), value in pair_counts.items():
        counts[char1] += value

    counts[original_polymer[-1]] += 1

    if as_sorted_list:
        return sorted(((char, count) for char, count in counts.items()), key=lambda t: t[1])

    return counts
