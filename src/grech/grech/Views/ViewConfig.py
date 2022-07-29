from rich.table import Column
from rich.progress import Progress, BarColumn, TextColumn
from rich.text import Text
from rich.console import Console
from rich.table import Table

from grech.Model.config.UserConfig import UserConfigList


class ViewConfig:
    def __init__(self, title="設定内容", col_name="項目", col_value="値") -> None:
        self.title = title
        self.col_name = col_name
        self.col_value = col_value
        pass

    def view(self, user_config_list: UserConfigList) -> Table:
        table = Table(title=self.title, show_lines=True)
        table.add_column(self.col_name, justify="right", style="cyan", no_wrap=True)
        table.add_column(self.col_value, style="magenta")
        for data in user_config_list.list:
            table.add_row(data.name, data.value)
        return table
