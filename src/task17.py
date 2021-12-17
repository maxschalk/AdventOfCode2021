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
    pattern = re.compile(r"target area: x=(-?[0-9]+)\.{2}(-?[0-9]+), y=(-?[0-9]+)\.{2}(-?[0-9]+)")

    line = data[0]

    result = pattern.match(line).groups()

    x_start, x_end, y_start, y_end = tuple(map(int, result))

    if abs(x_start) > abs(x_end):
        x_start, x_end = x_end, x_start

    if abs(y_start) > abs(y_end):
        y_start, y_end = y_end, y_start

    return (x_start, x_end, y_start, y_end)


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


def _solve_part_one(target_area):
    *_, y_end = target_area
    return sum(range(0, abs(y_end)))


def _solve_part_two(target_area):
    min_xv, max_xv, min_yv, max_yv = velocity_ranges(target_area)

    possibilities = set()

    for xv in range(min_xv, max_xv + 1):
        for yv in range(min_yv, max_yv + 1):
            if can_reach_target((xv, yv), target_area):
                possibilities.add((xv, yv))

    return len(possibilities)


def velocity_ranges(target_area):
    x_start, x_end, y_start, y_end = target_area

    min_yv = y_end
    max_yv = abs(y_end)

    min_xv = 0
    x_reach = x_start

    while x_reach > 0:
        min_xv += 1
        x_reach -= min_xv

    max_xv = x_end

    return min_xv, max_xv, min_yv, max_yv


def can_reach_target(velocity, target_area):
    probe = (0, 0)
    xv, yv = velocity

    while not probe_missed_target(probe, target_area):
        if probe_in_target(probe, target_area):
            return True

        x, y = probe
        probe = (x + xv, y + yv)

        xv = max(xv - 1, 0)
        yv -= 1

    return False


def probe_in_target(probe_pos, target_area):
    x, y = probe_pos
    x_start, x_end, y_start, y_end = target_area

    return x_start <= x <= x_end and y_end <= y <= y_start


def probe_missed_target(probe_pos, target_area):
    return probe_below_target(probe_pos, target_area) or probe_passed_target(probe_pos, target_area)


def probe_below_target(probe_pos, target_area):
    _, y = probe_pos
    *_, y_end = target_area

    return y < y_end


def probe_passed_target(probe_pos, target_area):
    x, _ = probe_pos
    _, x_end, *_ = target_area

    return abs(x) > abs(x_end)
