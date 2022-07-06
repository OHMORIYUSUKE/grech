import os
import yaml
import sys

def open_yaml(file_name: str) -> object:
  with open(f"{os.getcwd()}/../{file_name}") as file:
    obj = yaml.safe_load(file)
    return obj

def main():
  obj = open_yaml("test.yml")
  print(obj["name"])

if __name__ == '__main__':
  main()