import urllib.request, urllib.error
import sys
import subprocess
from subprocess import PIPE,TimeoutExpired

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
    
    def check_status(self, command="", regexp="") -> object:
        run_cmd = f"{command} {regexp}"
        proc = subprocess.run(f"{command} {regexp}", timeout=100, shell=True, stdout=PIPE, stderr=PIPE, text=True)
        return {'out': proc.stdout,'error': proc.stderr, 'run_cmd': run_cmd}

    def env_var_constructor(self, loader, node):
        ENV_PATTERN = re.compile(r'\$\{(.*)\}')
        ENV_TAG = '!env_var'
        value = loader.construct_scalar(node)
        matched = ENV_PATTERN.match(value)
        if matched is None:
            return value
        proto = matched.group(1)
        new_dir_path = "/etc/os_lecture_support_tool"
        config = configparser.ConfigParser()
        config.read(f'{new_dir_path}/config.ini')
        obj = Lib().open_yaml(file_path=config['user']['yaml'])
        yaml_data = yaml.safe_load(obj)
        env_val = os.environ[proto] if proto in os.environ else yaml_data["config"][proto]
        return env_val