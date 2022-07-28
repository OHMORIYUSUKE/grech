from rich.table import Column
from rich.progress import Progress, BarColumn, TextColumn
from rich.text import Text
from rich.console import Console
from rich.table import Table

from os_lecture_support_tool.Model.result.TestResultTable import TestResultTable


class ViewResult:
    def __init__(
        self,
        debug_mode=False,
        title="結果",
        col_chapter="チャプター",
        col_name="項目",
        col_cmd="コマンド",
        col_message="コメント",
    ) -> None:
        self.debug_mode = debug_mode
        self.title = title
        self.col_chapter = col_chapter
        self.col_name = col_name
        self.col_cmd = col_cmd
        self.col_message = col_message
        pass

    def view(self, test_result_table_data: TestResultTable) -> Table:
        table = Table(title=self.title, show_lines=True)
        table.add_column(self.col_chapter, justify="right", style="white", no_wrap=True)
        table.add_column(self.col_name, style="cyan", no_wrap=True)
        if self.debug_mode:
            table.add_column(self.col_cmd, style="magenta")
        table.add_column(self.col_message, style="green", overflow="fold")
        if self.debug_mode:
            for data in test_result_table_data.result:
                if data.status == 0:
                    table.add_row(
                        data.chapter,
                        data.name,
                        data.cmd,
                        Text().append("よくできました!", style="bold green"),
                    )
                else:
                    table.add_row(
                        data.chapter,
                        data.name,
                        data.cmd,
                        Text().append(data.message, style="bold red"),
                    )
        else:
            for data in test_result_table_data.result:
                if data.status == 0:
                    table.add_row(
                        data.chapter,
                        data.name,
                        Text().append("よくできました!", style="bold green"),
                    )
                else:
                    table.add_row(
                        data.chapter,
                        data.name,
                        Text().append(data.message, style="bold red"),
                    )
        return table
