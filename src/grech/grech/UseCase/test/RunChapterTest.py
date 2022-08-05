from typing import TypeVar, Union
from rich.progress import track

from grech.Model.result.TestResultTable import (
    TestResultRow,
    TestResultTable,
)
from grech.Model.test.Test import Test, Regexp

from grech.UseCase.test.TestSetUp import TestSetUp

from grech.UseCase.test.RunTest import RunTest


class RunChapterTest:
    def __init__(self) -> None:
        pass

    def run_test_chapter(self, chapter_name: str) -> Union[TestResultTable, None]:
        yaml_data = TestSetUp().init()
        result_rows = []
        for chapter_name_data in yaml_data["check"].keys():
            if chapter_name == chapter_name_data:
                for test_data in track(
                    yaml_data["check"][chapter_name_data],
                    description="実行中...🚧",
                    finished_style="green",
                    complete_style="green",
                ):
                    print(f"・{test_data['name']} を確認中...")
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
        if len(result_rows) == 0:
            return None
        return TestResultTable(result=result_rows)
