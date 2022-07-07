from fire import Fire
import sys
import configparser
import os
import yaml
import asyncio
from termcolor import colored
import json

from os_lecture_support_tool.lib.lib import Lib

class Config:
    """設定を行います。"""
    def yaml(self, file):
        """チェックする項目が記載されたYAMLファイルの場所を設定します。 --set {URL}"""
        config = configparser.ConfigParser()
        config['user'] = {
            'yaml': file
        }
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
            print(f'yaml:{config["user"]["yaml"]}')
        except:
            print("設定がされていません。")
            sys.exit(1)

class Check:
    """課題の状態を確認することができます。"""
    def all(self):
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
        # print(json.dumps(yaml_data, indent = 2, ensure_ascii=False))
        for data in yaml_data["check"].keys():
            print(data)
            for data2 in yaml_data["check"][data]:
                # 確認
                print(data2["name"])
                regexp_string = ""
                if data2["regexp"]["type"] == "and":
                    for i, data3 in enumerate(data2["regexp"]["list"]):
                        regexp_string = regexp_string + " | grep " + data3
                elif data2["regexp"]["type"] == "or":
                    for i, data3 in enumerate(data2["regexp"]["list"]):
                        regexp_string = regexp_string + " grep -e " + data3
                command_response = Lib().check_status(command=data2["cmd"], regexp=regexp_string)
                print(command_response["run_cmd"])
                print(command_response["out"])
                print(command_response["error"])
        sys.exit(0)
    def chapter(self, n=1):
        """任意のチャプターまで終了しているか確認します。(--n {チャプター番号})"""
        return n

class Command:
    config = Config
    check = Check

def main():
  Fire(Command)

if __name__ == '__main__':
  main()