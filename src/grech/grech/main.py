from fire import Fire

from grech.Controller.CheckController import Check
from grech.Controller.ConfigController import Config
from grech.Controller.InfoController import Info


class Command:
    config = Config
    check = Check
    info = Info


def main():
    Fire(Command)


if __name__ == "__main__":
    main()
