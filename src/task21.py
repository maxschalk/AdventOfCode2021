import re

from pathlib import Path
from contextlib import suppress
from typing import Dict, Tuple

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

    return content


def parse_input(data, test):
    pattern = re.compile(r"Player \d+ starting position: (\d+)")

    result = pattern.findall(data)

    return tuple(map(int, result))


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

def _solve_part_one(starting_positions):
    p1, p2 = starting_positions
    positions = [p1 - 1, p2 - 1]
    scores = [0, 0]

    die = deterministic_dice()

    player1_turn = True

    turns = 0

    while True:
        turns += 1

        player_index = (1, 0)[player1_turn]

        for _ in range(3):
            positions[player_index] += next(die)

        positions[player_index] %= 10

        scores[player_index] += positions[player_index] + 1

        if scores[player_index] >= 1000:
            break

        player1_turn = not player1_turn

    lose, win = sorted(scores)
    return lose * turns * 3


def deterministic_dice():
    x = 0

    while True:
        yield x + 1
        x = (x + 1) % 100


class Universe:
    def __init__(self, positions, scores, player1_turn=True, existences=1):
        self.positions = positions
        self.scores = scores

        self.player1_turn = player1_turn

        self.existences = existences

        self.completed = False

    def to_key(self):
        return *self.positions, *self.scores, int(self.player1_turn)

    def is_completed(self):
        if self.completed:
            return True

        self.completed = any(map(lambda x: x >= 21, self.scores))

        return self.completed

    def winner(self):
        p1, p2 = self.scores
        return (0, p1) if p1 > p2 else (1, p2)

    def absorb_existences(self, other):
        self.existences += other.existences

    def spawn_universe_for_step(self, step_length, multiply_existences):
        player_index = (1, 0)[self.player1_turn]

        new_positions = self.positions[:]
        new_positions[player_index] += step_length
        new_positions[player_index] %= 10

        new_scores = self.scores[:]
        new_scores[player_index] += new_positions[player_index] + 1

        return Universe(new_positions, new_scores, not self.player1_turn, self.existences * multiply_existences)

    def __str__(self):
        return f"U[{self.existences}, pos={self.positions[0] + 1, self.positions[1] + 1}, score={self.scores}]"


def _solve_part_two(starting_positions):
    p1, p2 = starting_positions
    positions = [p1 - 1, p2 - 1]
    scores = [0, 0]

    initial_universe = Universe(positions, scores)

    running_universes: Dict[Tuple, Universe] = {initial_universe.to_key(): initial_universe}

    completed_universes: Dict[Tuple, Universe] = dict()

    # freq, steps
    universe_spawns = ((1, 3), (3, 4), (6, 5), (7, 6), (6, 7), (3, 8), (1, 9))

    while running_universes:
        new_running_universes = dict()

        for universe in running_universes.values():
            for freq, step in universe_spawns:
                new_universe = universe.spawn_universe_for_step(step_length=step, multiply_existences=freq)

                add_to = completed_universes if new_universe.is_completed() else new_running_universes

                if new_universe.to_key() in add_to:
                    add_to[new_universe.to_key()].absorb_existences(new_universe)
                else:
                    add_to[new_universe.to_key()] = new_universe

        running_universes = new_running_universes

    wins = [0, 0]

    for completed_universe in completed_universes.values():
        winner, _ = completed_universe.winner()

        wins[winner] += completed_universe.existences

    return max(wins)
