from fire import Fire

from os_lecture_support_tool.Controller.CheckController import Check
from os_lecture_support_tool.Controller.ConfigController import Config


class Command:
    config = Config
    check = Check


def main():
    Fire(Command)


if __name__ == "__main__":
    main()
