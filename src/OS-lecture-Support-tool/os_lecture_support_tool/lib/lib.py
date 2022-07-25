import urllib.request, urllib.error
import sys
import subprocess
from subprocess import PIPE, TimeoutExpired

import yaml
import re
import os
import configparser


class Lib:
    def open_yaml(self, file_path: str) -> object:
        try:
            f = urllib.request.urlopen(file_path)
            stdout = f.read()
            return stdout
        except urllib.request.HTTPError as e:
            stderrout = e.read()
            print(stderrout)
            sys.exit(1)

    def check_status(self, working_directory="", command="", regexp="") -> object:
        if working_directory == "":
            run_cmd = f"{command} {regexp}"
        else:
            run_cmd = f"cd {working_directory} && {command} {regexp}"
        proc = subprocess.run(
            f"{run_cmd}", timeout=100, shell=True, stdout=PIPE, stderr=PIPE, text=True
        )
        return {"out": proc.stdout, "error": proc.stderr, "run_cmd": run_cmd}

    def change_env_value(self, command=""):
        try:
            new_dir_path = "/etc/os_lecture_support_tool"
            config = configparser.ConfigParser()
            config.read(f"{new_dir_path}/config.ini")
            obj = Lib().open_yaml(file_path=config["user"]["yaml"])
        except:
            print("設定が読み込めませんでした。")
            sys.exit(1)
        yaml_data = yaml.safe_load(obj)
        for config_data in yaml_data["config"]:
            if config_data in command:
                command = re.sub(
                    "\$\{( *" + config_data + " *)\}",
                    config["user"][config_data],
                    command,
                )
        return command
