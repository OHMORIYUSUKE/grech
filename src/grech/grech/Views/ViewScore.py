from rich.table import Column
from rich.progress import Progress, BarColumn, TextColumn
from rich.text import Text
from rich.console import Console
from rich.table import Table

from grech.Model.result.ScoreTable import ScoreTable


class ViewScore:
    def __init__(
        self, title="スコア", col_chapter="チャプター", col_check="確認項目", col_score="スコア"
    ) -> None:
        self.title = title
        self.col_chapter = col_chapter
        self.col_check = col_check
        self.col_score = col_score
        pass

    def view(self, score_table_data: ScoreTable) -> Table:
        table = Table(title=self.title, show_lines=True)
        table.add_column(self.col_check, justify="right", style="white", no_wrap=True)
        table.add_column(self.col_check, style="cyan", no_wrap=True)
        table.add_column(self.col_score, justify="right", style="green", no_wrap=True)
        for data in score_table_data.result:
            table.add_row(
                data.chapter,
                self.__list2str(data.name),
                self.__all_test_ok(score=data.score, max_score=data.max_score),
            )
        return table

    def __list2str(self, list_data: list) -> str:
        str_data = ""
        for data in list_data:
            str_data += "・" + data + "\n"
        return str_data

    def __all_test_ok(self, score: int, max_score: int) -> str:
        if score == max_score:
            return str(score) + " / " + str(max_score) + "\n" + "⭕"
        else:
            return str(score) + " / " + str(max_score) + "\n" + "❌"
