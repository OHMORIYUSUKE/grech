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
        print(colored("❗入力せずにEnterを入力した場合は、設定がすでに設定されている値に設定されます❗", "yellow"))
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
        result_name = []
        result_value = []
        try:
            for data in config["user"]:
                result_name.append(data)
                result_value.append(config['user'][data])
                result_table_data = {"項目": result_name , "設定内容": result_value}
            print(tabulate(result_table_data, headers="keys", tablefmt='fancy_grid'))
            print(colored('設定済みの項目を表示しています。', 'green'))
        except:
            print(colored("設定がされていません。", 'red'))
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
                command_response = Lib().check_status(working_directory=data2["working-directory"]  ,command=Lib().change_env_value(data2["cmd"]), regexp=Lib().change_env_value(regexp_string))
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
                print(Lib().change_env_value(data2["cmd"]))

class Command:
    config = Config
    check = Check

def main():
  Fire(Command)

if __name__ == '__main__':
  main()