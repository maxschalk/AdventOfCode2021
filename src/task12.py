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
    out = []

    pattern = re.compile(r"([a-zA-Z]+)-([a-zA-Z]+)")

    for line in data:
        start, end = pattern.match(line).groups()
        out.append((start, end))

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

START = "start"
END = "end"


def _solve_part_one(data):
    connections = collections.defaultdict(list)

    for start, end in data:
        connections[start].append(end)
        connections[end].append(start)

    return len(all_paths(connections, True))


def all_paths(connections, small_cave_visited_twice=False):
    paths = []
    _all_paths(START, paths, connections, [START], small_cave_visited_twice)

    print("\n".join(map(str, paths)))
    return paths


def _all_paths(node, paths, connections, current_path, small_cave_visited_twice):
    if node == END:
        paths.append(current_path[:])
        return

    for step in connections[node]:
        if step == START:
            continue

        if step[0].islower() and step in current_path:
            if small_cave_visited_twice:
                continue
            else:
                current_path.append(step)
                _all_paths(step, paths, connections, current_path, True)
                current_path.pop()

        else:
            current_path.append(step)
            _all_paths(step, paths, connections, current_path, small_cave_visited_twice)
            current_path.pop()


def _solve_part_two(data):
    connections = collections.defaultdict(list)

    for start, end in data:
        connections[start].append(end)
        connections[end].append(start)

    return len(all_paths(connections, False))
