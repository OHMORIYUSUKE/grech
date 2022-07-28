from typing import Any
import urllib.request, urllib.error
import sys
import yaml

from os_lecture_support_tool.UseCase.config.ConfigSetUp import ConfigSetUp


class TestSetUp:
    def __init__(self) -> None:
        self.config = ConfigSetUp().init()
        pass

    def init(self) -> Any:
        yaml_path = self.config["user"]["yaml"]
        try:
            f = urllib.request.urlopen(yaml_path)
            obj = f.read()
            yaml_data = yaml.safe_load(obj)
            return yaml_data
        except urllib.request.HTTPError as e:
            stderrout = e.read()
            print(stderrout)
            sys.exit(1)
