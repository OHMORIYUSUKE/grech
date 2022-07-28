import configparser
import sys


class ConfigSetUp:
    def __init__(self) -> None:
        pass

    def init(self) -> configparser.ConfigParser:
        try:
            config = configparser.ConfigParser()
            new_dir_path = "/etc/os_lecture_support_tool"
            config.read(f"{new_dir_path}/config.ini")
            return config
        except:
            print("設定ファイルが読み込めませんでした。")
            sys.exit(1)
