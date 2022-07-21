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

class Config:
    """設定を行います。"""
    def set(self, file=""):
        """チェックする項目が記載されたYAMLファイルの場所を設定します。 --set {URL}"""
        config = configparser.ConfigParser()
        config_list = {}
        new_dir_path = "/etc/os_lecture_support_tool"
        config.read(f'{new_dir_path}/config.ini')
        try:
            # 初回実行時(引数なしは例外)
            obj = Lib().open_yaml(file_path=file)
            config_list["yaml"] = file
        except:
            if not file:      
                try:
                    # ２回目以降
                    obj = Lib().open_yaml(file_path=config['user']['yaml'])
                    config_list["yaml"] = config['user']['yaml']
                except:
                    # 初回実行時(引数なしは例外)(ここにジャンプ)
                    print(colored("❗初回設定時は`os_lecture_support_tool config set {yamlのURL}`を実行してください❗", "red"))
                    sys.exit(1) 
        yaml_data = yaml.safe_load(obj)
        print(colored("❗入力せずにEnterを入力した場合は、すでに設定されている値に設定されます❗", "yellow"))
        for data in yaml_data["config"]:
            config_data = ""
            try:
                config_data = config['user'][data]
            except:
                config_data = "未設定"
            config_string = input(f"{data}を入力してください(デフォルト:{yaml_data['config'][data]}, 現在の設定:{config_data}):")
            if not config_string:
                try:
                    config_string = config['user'][data]
                except:
                    config_string = yaml_data['config'][data]
            config_list[data] = config_string.replace('%', '%%')
        config['user'] = config_list
        try:
            new_dir_path = "/etc/os_lecture_support_tool"
            if not os.path.exists(new_dir_path):
                os.makedirs(new_dir_path)
            f = open(f'{new_dir_path}/config.ini', 'w')
            config.write(f)
            print(colored("設定を保存しました", "green"))
            sys.exit(0)
        except:
              sys.exit(1)
    def check(self):
        new_dir_path = "/etc/os_lecture_support_tool"
        config = configparser.ConfigParser()
        config.read(f'{new_dir_path}/config.ini')
        table = Table(title="設定内容", show_lines=True)
        table.add_column("項目", justify="right", style="cyan", no_wrap=True)
        table.add_column("値", style="magenta")
        try:
            for data in config["user"]:
                result_name = data
                result_value = config['user'][data]
                table.add_row(result_name, result_value)
            console = Console()
            console.print(table)
        except:
            print(colored("設定がされていません。", 'red'))
            sys.exit(1)

class Check:
    """課題の状態を確認することができます。"""
    def all(self, debug=0):
        """すべての課題が終了しているか確認します。"""
        try:
            new_dir_path = "/etc/os_lecture_support_tool"
            config = configparser.ConfigParser()
            config.read(f'{new_dir_path}/config.ini')
            obj = Lib().open_yaml(file_path=config['user']['yaml'])
        except:
            print("設定が読み込めませんでした。")
            sys.exit(1)
        # 結果
        score_sum = 0
        score = 0
        table_score = Table(title="スコア", show_lines=True)
        table_score.add_column("チャプター", justify="right", style="white", no_wrap=True)
        table_score.add_column("確認項目", style="cyan", no_wrap=True)
        table_score.add_column("スコア", justify="right", style="green", no_wrap=True)
        # 
        yaml_data = yaml.safe_load(obj)
        table = Table(title="結果", show_lines=True)
        table.add_column("チャプター", justify="right", style="white", no_wrap=True)
        table.add_column("項目", style="cyan", no_wrap=True)
        if debug:
            table.add_column("コマンド", style="magenta")
        table.add_column("コメント", style="green", overflow="fold")
        for data in yaml_data["check"].keys():
            result_name = ""
            result_cmd = ""
            result_message = ""
            score_sum = 0
            score = 0
            score_name = ""
            for i ,data2 in enumerate(yaml_data["check"][data]):
                result_name = data2["name"]
                regexp_string = ""
                if data2["regexp"][0]["type"] == "and":
                    regexp_string = ""
                    for i, data3 in enumerate(data2["regexp"][1]["list"]):
                        regexp_string = regexp_string + " | grep '" + data3 + "'"
                elif data2["regexp"][0]["type"] == "or":
                    regexp_string = " | grep"
                    for i, data3 in enumerate(data2["regexp"][1]["list"]):
                        regexp_string = regexp_string + " -e " + "'" + data3 + "'"
                command_response = Lib().check_status(working_directory=data2["working-directory"]  ,command=Lib().change_env_value(data2["cmd"]), regexp=Lib().change_env_value(regexp_string))
                if command_response["out"]:
                    result_message = Text()
                    result_message.append("よくできました!", style="bold green")
                    score = score + 1
                else:
                    result_message = Text()
                    result_message.append(f"間違っています...\n💡\n{data2['message']}", style="bold red")
                    score_name = result_name + "\n" + score_name
                if debug:
                    result_cmd = "$ " + command_response["run_cmd"] + "\n" + command_response["out"] + command_response["error"]
                    table.add_row(data, result_name, result_cmd, result_message)
                else:
                    table.add_row(data, result_name, result_message)
                score_sum = score_sum + 1
            table_score.add_row(data, score_name, str(score) + " / " + str(score_sum))
        console = Console()
        console.print(table)
        # 結果
        console = Console()
        console.print(table_score)
        sys.exit(0)

    def chapter(self, name="", debug=0):
        """任意のチャプターまで終了しているか確認します。(--n {チャプター名})"""
        try:
            new_dir_path = "/etc/os_lecture_support_tool"
            config = configparser.ConfigParser()
            config.read(f'{new_dir_path}/config.ini')
            obj = Lib().open_yaml(file_path=config['user']['yaml'])
        except:
            print("設定が読み込めませんでした。")
            sys.exit(1)
        yaml_data = yaml.safe_load(obj)
        # print(json.dumps(yaml_data, indent = 2, ensure_ascii=False))
        table = Table(title=f"{name} までの結果", show_lines=True)
        table.add_column("チャプター", justify="right", style="white", no_wrap=True)
        table.add_column("項目", style="cyan", no_wrap=True)
        if debug:
            table.add_column("コマンド", style="magenta")
        table.add_column("コメント", style="green", overflow="fold")
        for data in yaml_data["check"].keys():
            result_name = ""
            result_cmd = ""
            result_message = ""
            for data2 in yaml_data["check"][data]:
                result_name = data2["name"]
                regexp_string = ""
                if data2["regexp"][0]["type"] == "and":
                    regexp_string = ""
                    for i, data3 in enumerate(data2["regexp"][1]["list"]):
                        regexp_string = regexp_string + " | grep '" + data3 + "'"
                elif data2["regexp"][0]["type"] == "or":
                    regexp_string = " | grep"
                    for i, data3 in enumerate(data2["regexp"][1]["list"]):
                        regexp_string = regexp_string + " -e " + "'" + data3 + "'"
                command_response = Lib().check_status(working_directory=data2["working-directory"]  ,command=Lib().change_env_value(data2["cmd"]), regexp=Lib().change_env_value(regexp_string))
                if command_response["out"]:
                    result_message = Text()
                    result_message.append("よくできました!", style="bold green")
                else:
                    result_message = Text()
                    result_message.append(f"間違っています...\n💡\n{data2['message']}", style="bold red")
                if debug:
                    result_cmd = "$ " + command_response["run_cmd"] + "\n" + command_response["out"] + command_response["error"]
                    table.add_row(data, result_name, result_cmd, result_message)
                else:
                    table.add_row(data, result_name, result_message)
            if name == data:
                console = Console()
                console.print(table)
        sys.exit(0)

class Command:
    config = Config
    check = Check

def main():
  Fire(Command)

if __name__ == '__main__':
  main()