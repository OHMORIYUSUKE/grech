from typing import Any, List
from grech.Model.config.UserConfig import UserConfig, UserConfigList

from grech.UseCase.config.ConfigSetUp import ConfigSetUp

import urllib.request, urllib.error
import sys
import yaml
import os


class SetConfig:
    def __init__(self) -> None:
        self.config_dir_path = "/etc/grech"
        pass

    def check_exist_config_file(self, file_path: str) -> UserConfigList:
        try:
            ConfigSetUp().init()["user"]["yaml"]
            # 2回目以降の設定
            return self.__set_config_fix()
        except:
            # 初めての設定
            return self.__set_config_init(file_path=file_path)

    # 初期設定
    def __set_config_init(self, file_path: str) -> UserConfigList:
        if file_path == "":
            print("初回設定時はURLを引数に与えてください。`config set http://...yaml`")
            sys.exit(1)
        os.mkdir(self.config_dir_path)
        config_list = self.__find_config_list_in_yaml(file_path=file_path)
        result_list = []
        for data in config_list:
            input_value = input(f"{data.name}を入力してください(デフォルト:{data.value}, 現在の設定:未設定):")
            if input_value == "":
                input_value = data.value
            result_list.append(UserConfig(name=data.name, value=input_value))
        self.__save_config(
            file_path=file_path, config_list=UserConfigList(list=result_list)
        )
        return UserConfigList(list=result_list)

    # 2回目以降の設定(URL不要)
    def __set_config_fix(self) -> UserConfigList:
        file_path = ConfigSetUp().init()["user"]["yaml"]
        config_list = self.__find_config_list_in_yaml(file_path=file_path)
        result_list = []
        for data in config_list:
            input_value = input(
                f"{data.name}を入力してください(デフォルト:{data.value}, 現在の設定:{self.__find_set_config_value(name=data.name)}):"
            )
            if input_value == "":
                input_value = self.__find_set_config_value(name=data.name)
            result_list.append(UserConfig(name=data.name, value=input_value))
        self.__save_config(
            file_path=file_path, config_list=UserConfigList(list=result_list)
        )
        return UserConfigList(list=result_list)

    # 設定を保存
    def __save_config(self, file_path: str, config_list: UserConfigList) -> bool:
        try:
            f = open(f"{self.config_dir_path}/config.ini", "w")
            config = ConfigSetUp().init()
            config["user"] = {}
            config["user"]["yaml"] = file_path
            for data in config_list.list:
                config["user"][data.name] = data.value
            config.write(f)
            return True
        except:
            print("設定の書き込みに失敗しました。")
            return False

    # すでに設定されている値を取得
    def __find_set_config_value(self, name: str) -> str:
        config = ConfigSetUp().init()
        for data in config["user"]:
            if data.upper() == name:
                return config["user"][name]

    # 設定されていないデフォルト値
    def __find_config_list_in_yaml(self, file_path: str) -> List[UserConfig]:
        yaml_data = self.__read_yaml(file_path=file_path)
        result_list = []
        for name in yaml_data["config"]:
            value = yaml_data["config"][name]
            result_list.append(UserConfig(name=name, value=value))
        return result_list

    def __read_yaml(self, file_path: str) -> Any:
        try:
            f = urllib.request.urlopen(file_path)
            obj = f.read()
            yaml_data = yaml.safe_load(obj)
            return yaml_data
        except urllib.request.HTTPError as e:
            stderrout = e.read()
            print("指定されたURLは存在しない可能性があります。")
            sys.exit(1)
