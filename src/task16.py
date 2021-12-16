import functools
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
    if test:
        return data

    return data[0]


def solve_test(data):
    with suppress(NotImplementedError):
        for line in data:
            print(f"Part 1: {line}: {_solve_part_one(line)}")

        print('-' * 30)

        for line in data:
            print(f"Part 2: {line}: {_solve_part_two(line)}")


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
    packet = decode_msg(data)

    return sum_version_numbers(packet)


def _solve_part_two(data):
    packet = decode_msg(data)

    return eval_packet(packet)


def decode_msg(bits):
    bits = translate(bits)

    bits, packet = parse_next_packet(bits)

    return packet


def translate(hex_str):
    return str.join('', map(lambda c: bin(int(c, 16))[2:].zfill(4), hex_str))


def parse_next_packet(bits):
    packet_version, packet_type_id, packet_length_type_id = parse_header(bits[:7])

    packet_is_literal = packet_length_type_id is None

    if packet_is_literal:
        bits = bits[6:]

        bits, value = parse_literal_value_packet(bits)

        packet = ((packet_version, packet_type_id), value)
    else:
        bits = bits[7:]

        bits, value = parse_operator_packet(bits, packet_length_type_id)

        packet = ((packet_version, packet_type_id), value)

    return bits, packet


def parse_header(header):
    packet_version = int(header[:3], 2)
    packet_type_id = int(header[3:6], 2)

    if packet_type_id == 4:
        packet_length_id = None
    else:
        packet_length_id = header[6]

    return packet_version, packet_type_id, packet_length_id


def parse_literal_value_packet(data):
    index = 0

    bits = []

    while True:
        prefix, *number_bits = data[index:index + 5]

        bits += number_bits

        index += 5

        if prefix == '0':
            break

    value = int(str.join('', bits), 2)

    return data[index:], value


def parse_operator_packet(data, packet_length_type_id):
    sub_packets = []

    if packet_length_type_id == '0':
        number_of_following_bits = int(data[:15], 2)
        data = data[15:]

        sub_data = data[:number_of_following_bits]

        data = data[number_of_following_bits:]

        while sub_data:
            sub_data, packet = parse_next_packet(sub_data)
            sub_packets.append(packet)

    else:
        number_of_sub_packets = int(data[:11], 2)
        data = data[11:]

        for i in range(number_of_sub_packets):
            data, sub_packet = parse_next_packet(data)

            sub_packets.append(sub_packet)

    return data, sub_packets


def sum_version_numbers(packet):
    result = 0

    (packet_version, _), value = packet
    result += packet_version

    if isinstance(value, list):
        for packet in value:
            result += sum_version_numbers(packet)

    return result


def sum_packet(value):
    return sum(map(eval_packet, value))


def product_packet(value):
    return functools.reduce(operator.mul, map(eval_packet, value), 1)


def minimum_packet(value):
    return min(map(eval_packet, value))


def maximum_packet(value):
    return max(map(eval_packet, value))


def literal_value(value):
    return value


def greater_than(value):
    packet1, packet2 = value
    return int(eval_packet(packet1) > eval_packet(packet2))


def less_than(value):
    packet1, packet2 = value
    return int(eval_packet(packet1) < eval_packet(packet2))


def equal_to(value):
    packet1, packet2 = value
    return int(eval_packet(packet1) == eval_packet(packet2))


def eval_packet(packet):
    (_, packet_type_id), value = packet

    return FUNCS[packet_type_id](value)


FUNCS = {
    0: sum_packet,
    1: product_packet,
    2: minimum_packet,
    3: maximum_packet,
    4: literal_value,
    5: greater_than,
    6: less_than,
    7: equal_to,
}
