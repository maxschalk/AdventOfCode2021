import re

from collections import defaultdict
from pathlib import Path
from contextlib import suppress

from PATHS import TASK_INPUT_DIR, TEST_INPUT_DIR
from src.task08_objects import SignalMapping, SignalMappingSet

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
    unique_lengths = {2, 4, 3, 7}  # 1, 4, 7, 8
    count = 0

    for _, outputs in data:
        for output_len in map(len, outputs):
            count += output_len in unique_lengths

    return count


def _solve_part_two(data):
    return sum(decode_line(inputs, outputs) for inputs, outputs in data)


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


def decode_line(inputs, outputs):
    signal_mappings = create_signal_mappings(inputs)

    sm_set = SignalMappingSet("abcdefg", *signal_mappings)

    sm_set.reduce_all()

    solution = sm_set.get_all_unambiguous(as_dict=True)

    translation = translate_outputs(outputs, solution)

    result = ''.join(str(SIGNAL_TO_DIGIT_MAP[frozenset(signal)]) for signal in translation)

    return int(result)


def create_signal_mappings(signals):
    digit_to_len_map = {digit: len(signals) for digit, signals in DIGIT_TO_SIGNAL_MAP.items()}

    len_to_digit_map = defaultdict(list)
    for digit, len_signals in digit_to_len_map.items():
        len_to_digit_map[len_signals].append(digit)

    signal_mappings = []

    for signals in signals:
        possible_digits = len_to_digit_map[len(signals)]

        if len(possible_digits) == 1:
            to_signal = DIGIT_TO_SIGNAL_MAP[possible_digits[0]]
        else:
            to_signal = [DIGIT_TO_SIGNAL_MAP[digit] for digit in possible_digits]

        signal_mappings.append(SignalMapping(from_signal=signals, to_signal=to_signal))

    return signal_mappings


def translate_outputs(outputs, solution):
    return [str.join('', (solution[char] for char in output)) for output in outputs]
