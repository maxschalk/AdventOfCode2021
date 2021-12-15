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
    return data


def solve_test(data):
    with suppress(NotImplementedError):
        print(f"Part 1 - {calc_power_consumption(data)}")

        print(f"Part 2 - {verify_life_support_rating(data)}")


def solve_part_one(data):
    print(calc_power_consumption(data))


def solve_part_two(data):
    print(verify_life_support_rating(data))


def main(test=False):
    global TEST
    TEST = test

    data = read_input()
    data = normalize_input(data)

    if TEST:
        solve_test(data)
    else:
        solve_part_one(data)
        solve_part_two(data)


if __name__ == '__main__':
    main()


# LOGIC / SOLUTION

def count_bit_occurences(data, position=None):
    if position is None:
        return _count_all_bit_positions(data)

    return _count_single_bit_position(data, position)


def _count_all_bit_positions(data):
    bits = len(data[0])
    bit_counts = [[0, 0] for _ in range(bits)]

    for line in data:
        for bit, count in zip(line, bit_counts):
            count[int(bit)] += 1

    return bit_counts


def _count_single_bit_position(data, position):
    if position >= len(data[0]):
        raise ValueError("Position out of bounds")

    bit_counts = [0, 0]

    for line in data:
        bit_counts[int(line[position])] += 1

    return bit_counts


def calc_power_consumption(data):
    bit_counts = count_bit_occurences(data)

    most_common_bits = [('0', '1')[c1 > c0] for c0, c1 in bit_counts]

    gamma_rate = str.join('', most_common_bits)

    epsilon_rate = str.join('', ('1' if c == '0' else '0' for c in gamma_rate))

    return int(gamma_rate, 2) * int(epsilon_rate, 2)


def verify_life_support_rating(data):
    filtered_data = data[:]

    for i in range(len(filtered_data[0])):
        bit_counts = count_bit_occurences(filtered_data, i)

        c0, c1 = bit_counts

        most_common_bit = '0' if c0 > c1 else '1'

        filtered_data = list(filter(lambda b: b[i] == most_common_bit, filtered_data))

        if len(filtered_data) == 1:
            break

    oxygen_generator_rating, *_ = filtered_data

    filtered_data = data[:]

    for i in range(len(filtered_data[0])):
        bit_counts = count_bit_occurences(filtered_data, i)

        c0, c1 = bit_counts

        least_common_bit = '1' if c1 < c0 else '0'

        filtered_data = list(filter(lambda b: b[i] == least_common_bit, filtered_data))

        if len(filtered_data) == 1:
            break

    co2_scrubber_rating, *_ = filtered_data

    return int(oxygen_generator_rating, 2) * int(co2_scrubber_rating, 2)



