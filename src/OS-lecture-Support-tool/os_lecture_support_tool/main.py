from fire import Fire
import sys
import configparser
import os
import yaml

from os_lecture_support_tool.lib.lib import Lib

class Config:
    """設定を行います。"""
    def yaml(self, file):
        """チェックする項目が記載されたYAMLファイルの場所を設定します(デフォルトは'')"""
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

class Check:
    """課題の状態を確認することができます。"""
    def all(self):
        """すべての課題が終了しているか確認します。"""
        try:
            new_dir_path = "/etc/os_lecture_support_tool"
            config = configparser.ConfigParser()
            config.read(f'{new_dir_path}/config.ini')
        except:
            print("設定が読み込めませんでした。")
            sys.exit(1)
        obj = Lib().open_yaml(file_path=config['user']['yaml'])
        yaml_data = yaml.safe_load(obj)
        print(yaml_data["name"])
        print(yaml_data["config"])
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