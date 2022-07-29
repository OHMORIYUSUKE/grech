from rich.console import Console

from grech.Model.testInfo.TestInfo import TestInfo
from grech.UseCase.testinfo.ReadTestInfo import ReadTestInfo
from grech.Views.ViewTestInfo import ViewTestInfo


class Info:
    """このテストの情報を確認することができます。"""

    def show(self):
        """このテストの情報を確認することができます。"""
        test_info = ReadTestInfo().read_test_info()
        table = ViewTestInfo().view(test_info=test_info)
        console = Console()
        console.print(table)
