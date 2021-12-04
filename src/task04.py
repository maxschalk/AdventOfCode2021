from pathlib import Path
from contextlib import suppress

from PATHS import INPUT_DIR, TEST_INPUT_DIR

FILE_STEM = Path(__file__).stem

INPUT_FILE = INPUT_DIR.joinpath(f"{FILE_STEM}_input.txt")
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
    number_draw, _, *board_lines = data

    number_draw = list(str.split(number_draw, ','))

    board_lines = list(map(str.split, filter(lambda x: bool(x), board_lines)))

    boards = []
    for i in range(0, len(board_lines), 5):
        boards.append(board_lines[i:i+5])

    return number_draw, boards


def solve_test(data):
    with suppress(NotImplementedError):
        print(f"Part 1 - {score_first_winning_board(data)}")

        print(f"Part 2 - {score_last_winning_board(data)}")


def solve(data):
    with suppress(NotImplementedError):
        solve_part_one(data)
        solve_part_two(data)


def solve_part_one(data):
    print(score_first_winning_board(data))


def solve_part_two(data):
    print(score_last_winning_board(data))


def main(test=False):
    global TEST
    TEST = test

    data = read_input()
    data = normalize_input(data)

    if TEST:
        solve_test(data)
    else:
        solve(data)


if __name__ == '__main__':
    main()


# LOGIC / SOLUTION

def score_first_winning_board(data):
    number_draw, boards = data

    board_marks = [[[False] * 5 for _ in range(5)] for _ in boards]

    winning_board_number = -1
    winning_number = -1

    for number in number_draw:
        for board_index, board in enumerate(boards):
            marks = board_marks[board_index]

            for row_index, row in enumerate(board):
                for num_index, num in enumerate(row):
                    if num == number:
                        marks[row_index][num_index] = True

            for i in range(5):
                if all(marks[i]) or all(marks[r][i] for r in range(5)):
                    winning_board_number = board_index
                    winning_number = number
                    break

            if winning_board_number >= 0:
                break

        else:
            continue

        break

    unmarked_sum = 0

    winning_board = boards[winning_board_number]
    winning_board_marks = board_marks[winning_board_number]

    for pair in zip(winning_board, winning_board_marks):
        nums, marks = pair

        for num, mark in zip(nums, marks):
            if not mark:
                unmarked_sum += int(num)

    return unmarked_sum * int(winning_number)


def score_last_winning_board(data):
    number_draw, boards = data

    board_marks = [[[False] * 5 for _ in range(5)] for _ in boards]
    board_wins = [False for _ in boards]

    last_winning_board_number = -1
    last_winning_number = -1

    for number in number_draw:
        for board_index, board in enumerate(boards):
            if board_wins[board_index]:
                continue

            marks = board_marks[board_index]

            for row_index, row in enumerate(board):
                for num_index, num in enumerate(row):
                    if num == number:
                        marks[row_index][num_index] = True

            for i in range(5):
                if all(marks[i]) or all(marks[r][i] for r in range(5)):
                    last_winning_board_number = board_index
                    last_winning_number = number
                    board_wins[board_index] = True

    unmarked_sum = 0

    winning_board = boards[last_winning_board_number]
    winning_board_marks = board_marks[last_winning_board_number]

    for pair in zip(winning_board, winning_board_marks):
        nums, marks = pair

        for num, mark in zip(nums, marks):
            if not mark:
                unmarked_sum += int(num)

    return unmarked_sum * int(last_winning_number)
