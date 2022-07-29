from typing import List

import subprocess, sys, re
import yaml
from subprocess import PIPE, TimeoutExpired

from grech.UseCase.test.TestSetUp import TestSetUp

from grech.Model.test.CmdResult import CmdResult
from grech.Model.test.Test import Test, Regexp
from grech.Model.result.TestResultTable import TestResultRow

from grech.UseCase.config.ReadConfig import ReadConfig


class RunTest:
    def __init__(self) -> None:
        pass

    def run_test(self, chapter_name: str, test_data: Test) -> TestResultRow:
        cmd_result = self.__run_cmd(test_data=test_data)
        if cmd_result.status == 1:
            message = "間違っています...\n💡\n" + test_data.message
        else:
            message = "よくできました!"
        return TestResultRow(
            chapter=chapter_name,
            name=test_data.name,
            cmd="$ " + cmd_result.cmd + "\n" + cmd_result.out_put,
            message=message,
            status=cmd_result.status,
        )

    def __run_cmd(self, test_data: Test) -> CmdResult:
        regexp_str = self.__create_grep(test_data.regexp)
        if test_data.working_directory == "":
            run_cmd = f"{self.__change_env_value(test_data.cmd)} {self.__change_env_value(regexp_str)}"
        else:
            run_cmd = f"cd {test_data.working_directory} && {self.__change_env_value(test_data.cmd)} {self.__change_env_value(regexp_str)}"
        proc = subprocess.run(
            f"{run_cmd}", timeout=100, shell=True, stdout=PIPE, stderr=PIPE, text=True
        )
        if proc.stderr == "":
            return CmdResult(cmd=run_cmd, out_put=proc.stdout, status=0)
        else:
            return CmdResult(cmd=run_cmd, out_put=proc.stderr, status=1)

    def __create_grep(self, regexp_data: Regexp) -> str:
        if regexp_data.type == "and":
            regexp_string = ""
            for i, data3 in enumerate(regexp_data.list):
                regexp_string = regexp_string + " | grep '" + data3 + "'"
            return regexp_string
        elif regexp_data.type == "or":
            regexp_string = " | grep"
            for i, data3 in enumerate(regexp_data.list):
                regexp_string = regexp_string + " -e " + "'" + data3 + "'"
            return regexp_string

    def __change_env_value(self, cmd: str) -> str:
        yaml_data = TestSetUp().init()
        for config_data in yaml_data["config"]:
            if config_data in cmd:
                cmd = re.sub(
                    "\$\{( *" + config_data + " *)\}",
                    ReadConfig().read_config(name=config_data).value,
                    cmd,
                )
        return cmd
