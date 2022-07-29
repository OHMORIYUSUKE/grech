from os_lecture_support_tool.Model.testInfo.TestInfo import TestInfo
from os_lecture_support_tool.UseCase.testinfo.ReadTestInfo import ReadTestInfo
from os_lecture_support_tool.Views.ViewTestInfo import ViewTestInfo

from rich.console import Console


class Info:
    """このテストの情報を確認することができます。"""

    def show(self):
        """このテストの情報を確認することができます。"""
        test_info = ReadTestInfo().read_test_info()
        table = ViewTestInfo().view(test_info=test_info)
        console = Console()
        console.print(table)
