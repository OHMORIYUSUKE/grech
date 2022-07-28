from typing import List
from pydantic import BaseModel


# コマンド実行結果
class CmdResult(BaseModel):
    cmd: str  # コマンド
    out_put: str  # コマンド実行結果
    status: int  # エラーか成功か
