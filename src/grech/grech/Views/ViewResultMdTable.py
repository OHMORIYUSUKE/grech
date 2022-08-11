from rich.table import Column
from rich.progress import Progress, BarColumn, TextColumn
from rich.text import Text
from rich.console import Console
from rich.table import Table

from tabulate import tabulate

import pandas as pd

from grech.Model.result.TestResultTable import TestResultTable


class ViewResultMdTable:
    def __init__(
        self,
        title="結果",
        col_chapter="チャプター",
        col_name="項目",
        col_cmd="コマンド",
        col_message="コメント",
    ) -> None:
        self.title = title
        self.col_chapter = col_chapter
        self.col_name = col_name
        self.col_cmd = col_cmd
        self.col_message = col_message
        pass

    def view(self, test_result_table_data: TestResultTable) -> pd.DataFrame:
        table = []
        for data in test_result_table_data.result:
            if data.status == 0:
                table.append(
                    {
                        self.col_chapter: data.chapter,
                        self.col_name: data.name,
                        self.col_cmd: "<br>".join(data.cmd.splitlines()),
                        self.col_message: "よくできました!",
                    }
                )
            else:
                table.append(
                    {
                        self.col_chapter: data.chapter,
                        self.col_name: data.name,
                        self.col_cmd: "<br>".join(data.cmd.splitlines()),
                        self.col_message: " ".join(data.message.splitlines()),
                    }
                )
        return pd.DataFrame(table)
