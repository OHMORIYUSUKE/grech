import os
import yaml
import sys
import urllib.request, urllib.error

def open_yaml(file_path: str) -> object:
  try:
    f = urllib.request.urlopen(file_path) 
    stdout = f.read()
    return stdout
  except urllib.request.HTTPError as e:
      stderrout = e.read()
      print(stderrout)
      exit

def main():
  args = sys.argv
  # リリース時は0にする
  file_path = args[1]
  print(file_path)
  yaml_data = open_yaml(file_path=file_path)
  print(yaml.safe_load(yaml_data))

if __name__ == '__main__':
  main()