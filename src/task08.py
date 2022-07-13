from __future__ import annotations

import re

from typing import List, Iterable, Optional, Dict
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




class SignalMappingSet:
    def __init__(self, signals: Iterable[str], *signal_mappings: SignalMapping):
        self.signals = set(signals)
        self.signal_mappings = [*signal_mappings]

        self.unresolved_signals = set(signals)

        self._update_unresolved_signals()

    def add_signal_mapping(self, signal_mapping: SignalMapping) -> None:
        self.signal_mappings.append(signal_mapping)
        self._update_unresolved_signals()

    def _update_unresolved_signals(self) -> None:
        if len(self.unresolved_signals) == 0:
            return

        for signal_mapping in self.signal_mappings:
            if signal_mapping.is_unambiguous():
                self.unresolved_signals -= signal_mapping.from_signal

    def is_unambiguous(self) -> bool:
        return len(self.unresolved_signals) == 0

    def reduce_all_by(self, signal_mapping: Optional[SignalMapping]) -> None:
        self.signal_mappings = list(map(lambda sm: sm - signal_mapping, self.signal_mappings))
        self._update_unresolved_signals()

    def reduce_all(self, single_iteration: bool = False) -> None:
        while not self.is_unambiguous():

            for signal_mapping in filter(SignalMapping._is_subtractable, self.signal_mappings):
                self.reduce_all_by(signal_mapping)
                # print(self)

            self._update_unresolved_signals()

            if single_iteration:
                break

    def get_all_unambiguous(self, as_dict: bool = False) -> List[SignalMapping] | Dict[str, str]:
        relevant_mappings = list(filter(SignalMapping.is_unambiguous, self.signal_mappings))

        if as_dict:
            return {str.join('', mapping.from_signal): str.join('', mapping.to_signal) for mapping in relevant_mappings}

        return relevant_mappings

    def _deepcopy(self) -> SignalMappingSet:
        return SignalMappingSet(set(self.signals), *self.signal_mappings)

    def __contains__(self, signal_mapping: SignalMapping) -> bool:
        return signal_mapping in self.signal_mappings

    def __str__(self) -> str:
        return (
                f"SignalMappingSet[ signals = {sorted(self.signals)}\n"
                + str.join('\n', map(lambda sm: f"\t{sm}", self.signal_mappings))
                + "\n]"
        )


class SignalMapping:
    def __init__(self, from_signal: str | set | frozenset,
                 to_signal: str | set | frozenset | Iterable[str | set | frozenset]):

        if isinstance(from_signal, str):
            from_signal = set(from_signal)

        if isinstance(to_signal, str | set | frozenset):
            to_signal = set(to_signal)
        else:
            to_signal = list(map(set, to_signal))

        self.from_signal = from_signal
        self.to_signal = to_signal

    def is_unambiguous(self) -> bool:
        single_from_signal = len(self.from_signal) == 1
        single_to_signal = self._single_to_possibility() and len(self.to_signal) == 1

        return single_from_signal and single_to_signal

    def _is_subtractable(self) -> bool:
        return self._single_to_possibility()

    def _single_to_possibility(self) -> bool:
        return isinstance(self.to_signal, set)

    def _deepcopy(self) -> SignalMapping:
        from_signal = set(self.from_signal)
        to_signal = set(self.to_signal) if self._single_to_possibility() else list(map(set, self.to_signal))

        return SignalMapping(from_signal, to_signal)

    def __eq__(self, other: SignalMapping) -> bool:
        return self.from_signal == other.from_signal and self.to_signal == other.to_signal

    def __lt__(self, other) -> bool:
        return self.from_signal < other.from_signal

    def __sub__(self, other: SignalMapping) -> SignalMapping:
        new_sm = self._deepcopy()

        if not other._is_subtractable():
            return new_sm

        if not other < new_sm:
            return new_sm

        if other == new_sm:
            return new_sm

        new_sm.from_signal -= other.from_signal

        if new_sm._single_to_possibility():
            new_sm.to_signal -= other.to_signal
        else:
            new_to_signal = []

            for signal in new_sm.to_signal:
                if other.to_signal < signal:
                    new_to_signal.append(signal - other.to_signal)

            if len(new_to_signal) == 1:
                new_sm.to_signal = new_to_signal.pop()
            else:
                new_sm.to_signal = new_to_signal

        return new_sm

    def __str__(self) -> str:
        fs = str.join('', sorted(self.from_signal))

        if self._single_to_possibility():
            ts = f"'{str.join('', sorted(self.to_signal))}'"
        else:
            temp = map(lambda s: f"'{str.join('', sorted(s))}'", self.to_signal)
            ts = f"{{{str.join(', ', temp)}}}"

        return f"SignalMapping['{fs}' -> {ts}]"

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
