from typing import List
from os_lecture_support_tool.Model.config.UserConfig import UserConfig, UserConfigList
from os_lecture_support_tool.UseCase.config.ConfigSetUp import ConfigSetUp


class ReadConfig:
    def __init__(self) -> None:
        self.config = ConfigSetUp().init()
        pass

    def read_config_all(self) -> UserConfigList:
        config_list = []
        for data in self.config["user"]:
            value = self.read_config(name=data)
            config_list.append(UserConfig(name=data, value=value.value))
        list_data = UserConfigList(list=config_list)
        return list_data

    def read_config(self, name: str) -> UserConfig:
        value = self.config["user"][name]
        return UserConfig(name=name, value=value)
