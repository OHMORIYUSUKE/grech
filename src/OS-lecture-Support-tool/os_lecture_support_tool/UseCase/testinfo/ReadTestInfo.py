from typing import Union
from typing import Any
from os_lecture_support_tool.Model.testInfo.TestInfo import TestInfo
from os_lecture_support_tool.UseCase.test.TestSetUp import TestSetUp


class ReadTestInfo:
    def __init__(self) -> None:
        pass

    def read_test_info(self) -> TestInfo:
        yaml_data = TestSetUp().init()
        return self.__find_test_info_in_yaml(yaml_data=yaml_data)

    def __find_test_info_in_yaml(self, yaml_data: Any) -> TestInfo:
        name = self.__is_set(name="name", yaml_data=yaml_data)
        description = self.__is_set(name="description", yaml_data=yaml_data)
        docs_url = self.__is_set(name="docs_url", yaml_data=yaml_data)
        author = self.__is_set(name="author", yaml_data=yaml_data)
        copyright = self.__is_set(name="copyright", yaml_data=yaml_data)
        return TestInfo(
            name=name,
            description=description,
            docs_url=docs_url,
            author=author,
            copyright=copyright,
        )

    def __is_set(self, name: str, yaml_data: Any) -> Union[None, str]:
        try:
            return yaml_data[name]
        except:
            return None
