import configparser


class SetUp:
    def __init__(self) -> None:
        pass

    def init(self) -> configparser.ConfigParser:
        config = configparser.ConfigParser()
        new_dir_path = "/etc/os_lecture_support_tool"
        config.read(f"{new_dir_path}/config.ini")
        return config
