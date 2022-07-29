from typing import Any
import urllib.request, urllib.error
import sys
import yaml
from termcolor import colored

from grech.UseCase.config.ConfigSetUp import ConfigSetUp


class TestSetUp:
    def __init__(self) -> None:
        self.config = ConfigSetUp().init()
        pass

    def init(self) -> Any:
        try:
            yaml_path = self.config["user"]["yaml"]
        except:
            print("初回設定時はURLを引数に与えてください。`config set http://...yaml`")
            sys.exit(1)
        try:
            f = urllib.request.urlopen(yaml_path)
            obj = f.read()
            yaml_data = yaml.safe_load(obj)
            return yaml_data
        except urllib.request.HTTPError as e:
            stderrout = e.read()
            print("URLに誤りがあります。")
            sys.exit(1)
