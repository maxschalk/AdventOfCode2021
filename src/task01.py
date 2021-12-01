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

    lines = map(str.strip, lines)

    return lines


def normalize_input(data):
    return list(map(int, data))


def solve(measurements):
    print(solve_part_one(measurements))
    print(solve_part_two_simple(measurements))


def main(test=False):
    data = read_input(test=test)
    data = normalize_input(data)
    solve(data)


if __name__ == '__main__':
    main()


# LOGIC / SOLUTION

def list_shift(l, value):
    l.append(value)

    return l.pop(0)


def solve_part_one(measurements):
    count = 0

    measurements = list(measurements)

    for current_elem, next_elem in zip(measurements, measurements[1:]):
        count += next_elem > current_elem

    return count


def solve_part_two_simple(measurements):
    count = 0

    measurements = list(measurements)

    window_length = 3

    prev_window = [0] + measurements[:window_length - 1]
    window = measurements[:window_length]

    for measurement in measurements[window_length + 1:]:
        list_shift(prev_window, window[-1])
        list_shift(window, measurement)

        count += sum(window) > sum(prev_window)

    return count


def solve_part_two_galaxybrain(measurements):
    count = 0

    window_length = 3

    prev_window = [0] * window_length
    window = [0] * window_length

    for i in range(window_length):
        measurement = measurements.__next__()

        list_shift(prev_window, value=measurement)
        list_shift(window, value=measurement)

    list_shift(window, measurements.__next__())

    for measurement in measurements[window_length + 1:]:
        list_shift(prev_window, window[-1])
        list_shift(window, measurement)
        count += sum(window) > sum(prev_window)

    count += sum(window) > sum(prev_window)

    return count


if __name__ == '__main__':
    main()
