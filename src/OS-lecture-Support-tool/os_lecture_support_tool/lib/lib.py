import urllib.request, urllib.error
import sys
import subprocess
from subprocess import PIPE,TimeoutExpired

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
        proc = subprocess.run(f"{command} | grep -E '{regexp}'", timeout=100, shell=True, stdout=PIPE, stderr=PIPE, text=True)
        return {'out': proc.stdout,'error': proc.stderr}