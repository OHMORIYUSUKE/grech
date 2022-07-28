from os_lecture_support_tool.Model.result.TestResultTable import (
    TestResultRow,
    TestResultTable,
)
from os_lecture_support_tool.Model.test.Test import Test, Regexp

from os_lecture_support_tool.UseCase.test.TestSetUp import TestSetUp

from os_lecture_support_tool.UseCase.test.RunTest import RunTest


class RunChapterTest:
    def __init__(self) -> None:
        pass

    def run_test_chapter(self, chapter_name: str) -> TestResultTable:
        yaml_data = TestSetUp().init()
        result_rows = []
        for chapter_name_data in yaml_data["check"].keys():
            if chapter_name == chapter_name_data:
                for test_data in yaml_data["check"][chapter_name_data]:
                    test_result = RunTest().run_test(
                        chapter_name=chapter_name_data,
                        test_data=Test(
                            name=test_data["name"],
                            cmd=test_data["cmd"],
                            working_directory=test_data["working-directory"],
                            regexp=Regexp(
                                type=test_data["regexp"][0]["type"],
                                list=test_data["regexp"][1]["list"],
                            ),
                            message=test_data["message"],
                        ),
                    )
                    result_rows.append(
                        TestResultRow(
                            chapter=test_result.chapter,
                            name=test_result.name,
                            cmd=test_result.cmd,
                            message=test_result.message,
                            status=test_result.status,
                        )
                    )
        return TestResultTable(result=result_rows)