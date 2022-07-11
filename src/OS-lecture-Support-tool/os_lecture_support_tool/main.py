from fire import Fire
import sys
import configparser
import os
import yaml
import asyncio
from termcolor import colored
import json
from tabulate import tabulate
import re

from os_lecture_support_tool.lib.lib import Lib

class Config:
    """設定を行います。"""
    def yaml(self, file):
        """チェックする項目が記載されたYAMLファイルの場所を設定します。 --set {URL}"""
        config = configparser.ConfigParser()
        config_list = {'yaml': file}
        new_dir_path = "/etc/os_lecture_support_tool"
        config.read(f'{new_dir_path}/config.ini')
        obj = Lib().open_yaml(file_path=config['user']['yaml'])
        yaml_data = yaml.safe_load(obj)
        print(yaml_data["config"])
        for data in yaml_data["config"]:
            config_string = input(f"{data}を入力してください:")
            config_list[data] = config_string
        config['user'] = config_list
        try:
            new_dir_path = "/etc/os_lecture_support_tool"
            if not os.path.exists(new_dir_path):
                os.makedirs(new_dir_path)
            f = open(f'{new_dir_path}/config.ini', 'w')
            config.write(f)
            print("設定を保存しました")
            sys.exit(0)
        except:
              sys.exit(1)
    def check(self):
        new_dir_path = "/etc/os_lecture_support_tool"
        config = configparser.ConfigParser()
        config.read(f'{new_dir_path}/config.ini')
        try:
            print(f'設定済みの項目を表示します。')
            for data in config["user"]:
                print(f"{data} => {config['user'][data]}")
        except:
            print("設定がされていません。")
            sys.exit(1)

class Check:
    """課題の状態を確認することができます。"""
    def all(self, out=0):
        """すべての課題が終了しているか確認します。"""
        try:
            new_dir_path = "/etc/os_lecture_support_tool"
            config = configparser.ConfigParser()
            config.read(f'{new_dir_path}/config.ini')
            obj = Lib().open_yaml(file_path=config['user']['yaml'])
        except:
            print("設定が読み込めませんでした。")
            sys.exit(1)
        yaml_data = yaml.safe_load(obj)
        result_table_data = []
        result_name_list = []
        result_cmd_list = []
        result_message_list = []
        # print(json.dumps(yaml_data, indent = 2, ensure_ascii=False))
        print(colored("結果", "green"))
        for data in yaml_data["check"].keys():
            result_name_list.append(data)
            result_cmd_list.append("")
            result_message_list.append("")
            for data2 in yaml_data["check"][data]:
                result_name_list.append(data2["name"])
                regexp_string = ""
                if data2["regexp"][0]["type"] == "and":
                    regexp_string = ""
                    for i, data3 in enumerate(data2["regexp"][1]["list"]):
                        regexp_string = regexp_string + " | grep " + data3
                elif data2["regexp"][0]["type"] == "or":
                    regexp_string = " | grep"
                    for i, data3 in enumerate(data2["regexp"][1]["list"]):
                        regexp_string = regexp_string + " -e " + data3
                command_response = Lib().check_status(command=data2["cmd"], regexp=regexp_string)
                if out:
                    result_cmd_list.append("$ " + command_response["run_cmd"] + "\n" + command_response["out"] + command_response["error"])
                else:
                    result_cmd_list.append("")
                if command_response["out"]:
                    result_message_list.append(colored(f"よくできました!", "green"))
                else:
                    result_message_list.append(colored(f"間違っています...\n\n💡ヒント💡\n{data2['message']}", "red"))
        if result_cmd_list[1] == "":
            result_table_data = {"項目": result_name_list, "メッセージ": result_message_list}
        else:
            result_table_data = {"項目": result_name_list,"コマンド": result_cmd_list,"メッセージ": result_message_list}
        print(tabulate(result_table_data, headers="keys", tablefmt='fancy_grid'))
        sys.exit(0)
    def chapter(self, n=1):
        """任意のチャプターまで終了しているか確認します。(--n {チャプター番号})"""
        try:
            new_dir_path = "/etc/os_lecture_support_tool"
            config = configparser.ConfigParser()
            config.read(f'{new_dir_path}/config.ini')
            obj = Lib().open_yaml(file_path=config['user']['yaml'])
        except:
            print("設定が読み込めませんでした。")
            sys.exit(1)
        yaml_data = yaml.safe_load(obj)
        ENV_PATTERN = re.compile(r'\$\{(.*)\}')
        for data in yaml_data["check"].keys():
            for data2 in yaml_data["check"][data]:
                for cmd in data2["cmd"]:
                    print(cmd)
                    print(re.sub('\$\{(.*)\}', 'root', cmd))
                    if "MYSQL_USER" in cmd:
                        print(re.sub('\$\{(.*)\}', 'root', cmd))
                    elif "MYSQL_PASS" in cmd:
                        print(re.sub('\$\{(.*)\}', 'pass', cmd))
        

class Command:
    config = Config
    check = Check

def main():
  Fire(Command)

if __name__ == '__main__':
  main()