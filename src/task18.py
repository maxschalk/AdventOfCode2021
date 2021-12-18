from __future__ import annotations

import itertools
import json
import math
import re

from typing import Union
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
    return [json.loads(line) for line in data]


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


"""
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
"""


# SOLUTION


class MutableInt(int):
    def __init__(self, value=0):
        self.value = int(value)

    def add(self, other):
        self.value += int(other)
        return self

    def __add__(self, other):
        return MutableInt(self.value + int(other))

    def __int__(self):
        return self.value

    def __lt__(self, other):
        return int(self) < int(other)

    def __le__(self, other):
        return int(self) <= int(other)

    def __eq__(self, other):
        return int(self) == int(other)

    def __gt__(self, other):
        return int(self) > int(other)

    def __ge__(self, other):
        return int(self) >= int(other)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"MutableInt[{self.value}]"


class Pair:
    def __init__(self, left, right, depth):
        self.left = left
        self.right = right

        self.depth = depth

    def leftmost_element(self):
        return self._outermost_element(0)

    def rightmost_element(self):
        return self._outermost_element(1)

    def _outermost_element(self, index):
        elem: Union[Pair, MutableInt] = self[index]

        if isinstance(elem, MutableInt):
            return elem

        return elem._outermost_element(index)

    def inc_depth(self):
        self.depth += 1

        l, r = self

        if isinstance(l, Pair):
            l.inc_depth()

        if isinstance(r, Pair):
            r.inc_depth()

    def dec_depth(self):
        self.depth -= 1

        l, r = self

        if isinstance(l, Pair):
            l.dec_depth()

        if isinstance(r, Pair):
            r.dec_depth()

    # EXPLOSION

    def self_needs_explode(self):
        return self.depth >= 4 and isinstance(self.left, MutableInt) and isinstance(self.right, MutableInt)

    def sub_pair_needs_explode(self):
        return ((isinstance(self.left, Pair) and self.left.any_needs_explode())
                or (isinstance(self.right, Pair) and self.right.any_needs_explode()))

    def any_needs_explode(self):
        return (self.self_needs_explode()
                or (isinstance(self.left, Pair) and self.left.any_needs_explode())
                or (isinstance(self.right, Pair) and self.right.any_needs_explode()))

    def explode(self):
        return True, (self.left, self.right)

    def explode_sub_pairs(self):
        explosion_happened = False
        left_explosion = None
        right_explosion = None

        if isinstance(self.left, Pair):
            if self.left.self_needs_explode():
                explosion_happened = True
                left_explosion, right_explosion = self.left
                self.left = MutableInt(0)
            else:
                explosion_happened, (left_explosion, right_explosion) = self.left.explode_sub_pairs()

            if right_explosion:
                if isinstance(self.right, Pair):
                    self.right.leftmost_element().add(right_explosion)
                else:
                    self.right.add(right_explosion)

                right_explosion = None

        if explosion_happened:
            return explosion_happened, (left_explosion, right_explosion)

        if isinstance(self.right, Pair):
            if self.right.self_needs_explode():
                explosion_happened = True
                left_explosion, right_explosion = self.right
                self.right = MutableInt(0)
            else:
                explosion_happened, (left_explosion, right_explosion) = self.right.explode_sub_pairs()

            if left_explosion:
                if isinstance(self.left, Pair):
                    self.left.rightmost_element().add(left_explosion)
                else:
                    self.left.add(left_explosion)

                left_explosion = None

        return explosion_happened, (left_explosion, right_explosion)

    # SPLIT

    def self_needs_split(self):
        return ((isinstance(self.left, MutableInt) and self.left >= 10)
                or (isinstance(self.right, MutableInt) and self.right >= 10))

    def sub_pair_needs_split(self):
        return ((isinstance(self.left, Pair) and self.left.any_needs_split())
                or (isinstance(self.right, Pair) and self.right.any_needs_split()))

    def any_needs_split(self):
        return (self.self_needs_split()
                or (isinstance(self.left, Pair) and self.left.any_needs_split())
                or (isinstance(self.right, Pair) and self.right.any_needs_split()))

    def split_rec(self):
        if isinstance(self.left, MutableInt):
            if self.left >= 10:
                new_left = MutableInt(math.floor(int(self.left) / 2))
                new_right = MutableInt(math.ceil(int(self.left) / 2))

                self.left = Pair(new_left, new_right, self.depth + 1)
                return True
        else:
            if self.left.split_rec():
                return True

        if isinstance(self.right, MutableInt):
            if self.right >= 10:
                new_left = MutableInt(math.floor(int(self.right) / 2))
                new_right = MutableInt(math.ceil(int(self.right) / 2))

                self.right = Pair(new_left, new_right, self.depth + 1)
                return True
        else:
            if self.right.split_rec():
                return True

        return False

    def __getitem__(self, index):
        return (self.left, self.right)[index]

    def __iter__(self):
        return iter((self.left, self.right))

    def __add__(self, other):
        old_depth = self.depth

        self.inc_depth()
        other.inc_depth()

        return Pair(self, other, old_depth)

    def __str__(self):
        return f"[{self.left}, {self.right}]"

    def __repr__(self):
        return f"P{self.depth}[{self.left!r}, {self.right!r}]"


def pair_of(ls, depth=0):
    return Pair(*map(lambda elem: _pair_element_of(elem, depth + 1), ls), depth=depth)


def deepcopy_pair(pair):
    return pair_of(json.loads(str(pair)))


def _pair_element_of(elem, depth):
    if isinstance(elem, list):
        return pair_of(elem, depth)
    else:
        return MutableInt(elem)


def _solve_part_one(data):
    data = map(pair_of, data)

    summands_iter = iter(data)
    result = next(summands_iter)

    for next_summand in summands_iter:
        result = reduce_pair(result + next_summand)

    return magnitude(result)


def _solve_part_two(data):
    data = map(pair_of, data)

    max_mag = 0

    for a, b in itertools.permutations(data, 2):
        max_mag = max(max_mag, magnitude(reduce_pair(a + b)))

    return max_mag


def reduce_pair(pair):
    change = True

    while change:
        if pair.any_needs_explode():
            pair = deepcopy_pair(pair)
            pair.explode_sub_pairs()
        elif pair.any_needs_split():
            pair.split_rec()
        else:
            change = False

    return pair


def magnitude(element):
    if isinstance(element, MutableInt):
        return int(element)

    left, right = element

    return 3 * magnitude(left) + 2 * magnitude(right)
