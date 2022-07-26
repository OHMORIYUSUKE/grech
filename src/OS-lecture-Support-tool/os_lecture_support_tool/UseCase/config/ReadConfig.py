from typing import List
from os_lecture_support_tool.model.config.UserConfig import UserConfig, UserConfigList
from os_lecture_support_tool.UseCase.config.SetUp import SetUp


class ReadConfig:
    def __init__(self) -> None:
        pass

    def read_config_all(self) -> UserConfigList:
        config_list = []
        config = SetUp.init(self=self)
        for data in config["user"]:
            value = ReadConfig.read_config(self=self, name=data)
            config_list.append(UserConfig(name=data, value=value.value))
        list_data = UserConfigList(list=config_list)
        return list_data

    def read_config(self, name: str) -> UserConfig:
        config = SetUp.init(self=self)
        value = config["user"][name]
        return UserConfig(name=name, value=value)
