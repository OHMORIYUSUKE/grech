from fire import Fire
import sys
import configparser
import os
import yaml
import asyncio
from termcolor import colored
from rich.table import Column
from rich.progress import Progress, BarColumn, TextColumn
from rich.text import Text
from rich.console import Console
from rich.table import Table
import json
import re

from os_lecture_support_tool.lib.lib import Lib


from os_lecture_support_tool.UseCase.config.ReadConfig import ReadConfig
from os_lecture_support_tool.Views.ViewConfig import ViewConfig
from os_lecture_support_tool.Views.ViewScore import ViewScore
from os_lecture_support_tool.Views.ViewResult import ViewResult

from os_lecture_support_tool.UseCase.test.RunAllTest import RunAllTest

from os_lecture_support_tool.UseCase.score.TotallingScore import TotallingScore
from os_lecture_support_tool.UseCase.test.RunChapterTest import RunChapterTest


class Config:
    """設定を行います。"""

    def set(self, file=""):
        """チェックする項目が記載されたYAMLファイルの場所を設定します。 --set {URL}"""
        config = configparser.ConfigParser()
        config_list = {}
        new_dir_path = "/etc/os_lecture_support_tool"
        config.read(f"{new_dir_path}/config.ini")
        try:
            # 初回実行時(引数なしは例外)
            obj = Lib().open_yaml(file_path=file)
            config_list["yaml"] = file
        except:
            if not file:
                try:
                    # ２回目以降
                    obj = Lib().open_yaml(file_path=config["user"]["yaml"])
                    config_list["yaml"] = config["user"]["yaml"]
                except:
                    # 初回実行時(引数なしは例外)(ここにジャンプ)
                    print(
                        colored(
                            "❗初回設定時は`os_lecture_support_tool config set {yamlのURL}`を実行してください❗",
                            "red",
                        )
                    )
                    sys.exit(1)
        yaml_data = yaml.safe_load(obj)
        print(colored("❗入力せずにEnterを入力した場合は、すでに設定されている値に設定されます❗", "yellow"))
        for data in yaml_data["config"]:
            config_data = ""
            try:
                config_data = config["user"][data]
            except:
                config_data = "未設定"
            config_string = input(
                f"{data}を入力してください(デフォルト:{yaml_data['config'][data]}, 現在の設定:{config_data}):"
            )
            if not config_string:
                try:
                    config_string = config["user"][data]
                except:
                    config_string = yaml_data["config"][data]
            config_list[data] = config_string.replace("%", "%%")
        config["user"] = config_list
        try:
            new_dir_path = "/etc/os_lecture_support_tool"
            if not os.path.exists(new_dir_path):
                os.makedirs(new_dir_path)
            f = open(f"{new_dir_path}/config.ini", "w")
            config.write(f)
            print(colored("設定を保存しました", "green"))
            sys.exit(0)
        except:
            sys.exit(1)

    def check(self):
        try:
            user_config_list = ReadConfig().read_config_all()
            table = ViewConfig().view(user_config_list=user_config_list)
            console = Console()
            console.print(table)
        except:
            print(colored("設定がされていません。", "red"))
            sys.exit(1)


class Check:
    """課題の状態を確認することができます。"""

    def all(self, debug=0):
        """すべての課題が終了しているか確認します。"""
        print("実行中...")
        test_result_table_data = RunAllTest().run_test_all()
        if debug == 1:
            table = ViewResult(debug_mode=True).view(
                test_result_table_data=test_result_table_data
            )
        else:
            table = ViewResult(debug_mode=False).view(
                test_result_table_data=test_result_table_data
            )
        console = Console()
        console.print(table)
        # スコア
        score_table_data = TotallingScore().totalling_score(
            test_result_table_data=test_result_table_data
        )
        score_table = ViewScore().view(score_table_data=score_table_data)
        console = Console()
        console.print(score_table)
        if score_table_data.status == False:
            print("見直しましょう。")
        else:
            print("よく頑張りました。")

    def chapter(self, name="", debug=0):
        """指定のチャプターが完了しているか確認します(--name チャプター名)"""
        print("実行中...")
        test_result_table_data = RunChapterTest().run_test_chapter(chapter_name=name)
        if debug == 1:
            table = ViewResult(debug_mode=True).view(
                test_result_table_data=test_result_table_data
            )
        else:
            table = ViewResult(debug_mode=False).view(
                test_result_table_data=test_result_table_data
            )
        console = Console()
        console.print(table)
        # スコア
        score_table_data = TotallingScore().totalling_score(
            test_result_table_data=test_result_table_data
        )
        score_table = ViewScore().view(score_table_data=score_table_data)
        console = Console()
        console.print(score_table)
        if score_table_data.status == False:
            print("見直しましょう。")
        else:
            print("よく頑張りました。")


class Command:
    config = Config
    check = Check


def main():
    Fire(Command)


if __name__ == "__main__":
    main()
