from pathlib import Path

ROOT_DIR = Path(__file__).parent

SRC_DIR = ROOT_DIR.joinpath("src")

INPUT_DIR = ROOT_DIR.joinpath("inputs")

TEST_INPUT_DIR = INPUT_DIR.joinpath("tests")
TASK_INPUT_DIR = INPUT_DIR.joinpath("tasks")

BOILERPLATE_FILE = SRC_DIR.joinpath("task00_boilerplate.py")
