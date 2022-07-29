import configparser
import sys


class ConfigSetUp:
    def __init__(self) -> None:
        pass

    def init(self) -> configparser.ConfigParser:
        try:
            config = configparser.ConfigParser()
            dir_path = "/etc/grech"
            config.read(f"{dir_path}/config.ini")
            return config
        except:
            print("設定ファイルが読み込めませんでした。")
            sys.exit(1)
