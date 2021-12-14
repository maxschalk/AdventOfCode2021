import re
from shutil import copyfile

from PATHS import ROOT_DIR, SRC_DIR, INPUT_DIR, TEST_INPUT_DIR, BOILERPLATE_FILE


def main():
    task_number = input("Task number > ").strip()

    if not task_number.isnumeric():
        raise ValueError(f"{task_number} is not a number")

    task_number = int(task_number)

    if task_number < 1 or task_number > 24:
        raise ValueError(f"Number must be between 1 - 24, but was {task_number}")

    task_number = str(task_number).zfill(2)

    input_file_path = INPUT_DIR.joinpath(f"task{task_number}_input.txt")

    with open(input_file_path.as_posix(), 'w') as file:
        pass

    test_input_file_path = TEST_INPUT_DIR.joinpath(f"task{task_number}_test_input.txt")

    with open(test_input_file_path.as_posix(), 'w') as file:
        pass

    script_file_path = SRC_DIR.joinpath(f"task{task_number}.py")

    copyfile(BOILERPLATE_FILE.as_posix(), script_file_path)

    with open(ROOT_DIR.joinpath("main.py"), "r+") as file:
        src_code = file.read()

        src_code = re.sub(r"src\.task\d{2}", f"src.task{task_number}", src_code)
        src_code = re.sub(r"test=False", "test=True", src_code)

        file.seek(0)
        file.write(src_code)


if __name__ == '__main__':
    main()
