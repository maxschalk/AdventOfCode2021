import collections
import itertools
import operator
import re

from pathlib import Path
from contextlib import suppress

from PATHS import TEST_INPUT_DIR, TASK_INPUT_DIR

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
    data = str.join('\n', data)

    out = []

    pattern = re.compile(r"--- scanner \d+ ---\n")

    for block in pattern.split(data):
        block = block.strip()
        if not block:
            continue

        lines = block.split('\n')

        lines = list(map(lambda line: list(map(int, line.split(','))), lines))

        out.append(lines)

    return out


def solve_test(data):
    with suppress(NotImplementedError):
        solved_scanners = get_solved_scanners(data)

        print(f"Part 1 - {_solve_part_one(solved_scanners)}")

        print('-' * 15)

        print(f"Part 2 - {_solve_part_two(solved_scanners)}")


def solve(data):
    with suppress(NotImplementedError):
        solved_scanners = get_solved_scanners(data)
        solve_part_one(solved_scanners)
        solve_part_two(solved_scanners)


def solve_part_one(data):
    print(_solve_part_one(data))


def solve_part_two(data):
    print(_solve_part_two(data))


# SOLUTION


class Scanner:
    MAX_ROTATIONS = 24
    all_scanners = []

    def __init__(self, beacons, position=None):
        self.position = position

        self.original_beacons = [tuple(beacon) for beacon in beacons]

        self.beacons = [tuple(beacon) for beacon in beacons]

        self.beacon_rotations = None
        self._performed_rotations = 0

        self.rotation_locked = False

        self.id = len(self.all_scanners)
        self.all_scanners.append(self)

    def rotate_beacons(self):
        if self.rotation_locked:
            raise Exception("Rotation is locked")

        if self._performed_rotations == self.MAX_ROTATIONS:
            self.reset_beacons()

        if self.beacon_rotations is None:
            self.beacon_rotations = list(map(possible_rotations, self.beacons))

        self.beacons = list(map(next, self.beacon_rotations))

        self._performed_rotations += 1

    def reset_beacons(self):
        self.beacons = [tuple(beacon) for beacon in self.original_beacons]

        self.beacon_rotations = None
        self._performed_rotations = 0

    def is_solved(self):
        return self.position is not None

    def lock_beacon_rotation(self):
        self.rotation_locked = True

    def resolved_beacons(self):
        beacons = [tuple(beacon) for beacon in self.beacons]
        beacons = list(map(lambda beacon: add_beacons(beacon, self.position), beacons))
        return beacons


def _solve_part_two(solved_scanners):
    max_dist = 0

    for a, b in itertools.combinations(solved_scanners, 2):
        max_dist = max(max_dist, manhattan_distance(a.position, b.position))

    return max_dist


def _solve_part_one(solved_scanners):
    unique_beacons = set()

    for solved_scanner in solved_scanners:
        for beacon in solved_scanner.resolved_beacons():
            unique_beacons.add(beacon)

    return len(unique_beacons)


def get_solved_scanners(data):
    scanners = map(Scanner, data)

    scanner0, *scanners = scanners

    scanner0.position = (0, 0, 0)

    solved_scanners = [scanner0]
    solved_stack = {scanner0}
    unsolved_scanners = list(scanners)

    while solved_stack:
        solved_scanner = solved_stack.pop()

        for unsolved_scanner in unsolved_scanners[:]:
            check_scanners_for_overlap(solved_scanner, unsolved_scanner)

            if unsolved_scanner.is_solved():
                solved_scanners.append(unsolved_scanner)
                solved_stack.add(unsolved_scanner)

                unsolved_scanners.remove(unsolved_scanner)

    return solved_scanners


def check_scanners_for_overlap(solved_scanner, unsolved_scanner):
    for _ in range(Scanner.MAX_ROTATIONS):
        distance_count = collections.defaultdict(int)

        for beacon0 in solved_scanner.beacons:

            for beacon1 in unsolved_scanner.beacons:
                distance = sub_beacons(beacon0, beacon1)
                distance_count[distance] += 1

        distance, count = max(distance_count.items(), key=lambda t: t[1])

        if count < 12:
            unsolved_scanner.rotate_beacons()
            continue

        unsolved_scanner.lock_beacon_rotation()
        unsolved_scanner.position = add_beacons(solved_scanner.position, distance)
        return


def manhattan_distance(a, b):
    return sum(map(lambda t: abs(operator.sub(*t)), zip(a, b)))


def sub_beacons(beacon1, beacon2):
    return tuple(map(lambda t: operator.sub(*t), zip(beacon1, beacon2)))


def add_beacons(beacon1, beacon2):
    return tuple(map(lambda t: operator.add(*t), zip(beacon1, beacon2)))


def possible_rotations(position):
    positions = set()

    # turn XY
    for _ in range(4):
        x, y, z = position
        position = (y, -x, z)

        # turn XZ
        for _ in range(4):
            x, y, z = position
            position = (z, y, -x)

            # turn YZ
            for _ in range(4):
                x, y, z = position
                position = (x, -z, y)

                if position in positions:
                    continue

                positions.add(position)
                yield position
