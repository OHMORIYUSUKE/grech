from fire import Fire
import sys
from termcolor import colored
from rich.console import Console

from os_lecture_support_tool.UseCase.config.ReadConfig import ReadConfig
from os_lecture_support_tool.Views.ViewConfig import ViewConfig
from os_lecture_support_tool.UseCase.config.SetConfig import SetConfig


class Config:
    """設定を行います。"""

    def set(self, file=""):
        """チェックする項目が記載されたYAMLファイルの場所を設定します。 --set {URL}"""
        print("入力しない場合は、デフォルト値または、すでに設定されている値になります。")
        SetConfig().check_exist_config_file(file_path=file)
        user_config_list = ReadConfig().read_config_all()
        table = ViewConfig().view(user_config_list=user_config_list)
        console = Console()
        console.print(table)
        print("上記の内容で、設定を保存しました。")

    def check(self):
        try:
            user_config_list = ReadConfig().read_config_all()
            table = ViewConfig().view(user_config_list=user_config_list)
            console = Console()
            console.print(table)
        except:
            print("初回設定時はURLを引数に与えてください。`config set http://...yaml`")
            sys.exit(1)
