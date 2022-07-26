from rich.table import Column
from rich.progress import Progress, BarColumn, TextColumn
from rich.text import Text
from rich.console import Console
from rich.table import Table

from os_lecture_support_tool.model.config.UserConfig import UserConfigList


class ViewConfig:
    def __init__(self) -> None:
        pass

    def view(self, user_config_list: UserConfigList) -> Table:
        table = Table(title="設定内容", show_lines=True)
        table.add_column("項目", justify="right", style="cyan", no_wrap=True)
        table.add_column("値", style="magenta")
        for data in user_config_list.list:
            table.add_row(data.name, data.value)
        return table
