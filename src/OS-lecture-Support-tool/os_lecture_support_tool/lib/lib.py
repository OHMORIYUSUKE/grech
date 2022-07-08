import urllib.request, urllib.error
import sys
import subprocess
from subprocess import PIPE,TimeoutExpired

import yaml
import re
import os

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
        default = None
        if len(proto.split(':')) > 1:
            env_key, default = proto.split(':')
        else:
            env_key = proto
        env_val = os.environ[env_key] if env_key in os.environ else default 
        return env_val