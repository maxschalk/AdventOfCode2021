import sys

from src.task19 import main as run_task


def main():
    if len(sys.argv) > 1:
        filename, test, *_ = sys.argv
    else:
        test = "True"

    run_task(test=eval(test))


if __name__ == '__main__':
    main()

