from rich.table import Column
from rich.progress import Progress, BarColumn, TextColumn
from rich.text import Text
from rich.console import Console
from rich.table import Table

from os_lecture_support_tool.Model.testInfo.TestInfo import TestInfo


class ViewTestInfo:
    def __init__(self, title="テストの情報", col_name="項目", col_value="値") -> None:
        self.title = title
        self.col_name = col_name
        self.col_value = col_value
        pass

    def view(self, test_info: TestInfo) -> Table:
        table = Table(title=self.title, show_lines=True)
        table.add_column(self.col_name, justify="right", style="cyan", no_wrap=True)
        table.add_column(self.col_value, style="magenta", overflow="fold")
        table.add_row("テスト名", test_info.name)
        table.add_row("説明", test_info.description)
        table.add_row("資料のURL", test_info.docs_url)
        table.add_row("テスト作成者", test_info.author)
        table.add_row("コピーライト", test_info.copyright)
        return table
