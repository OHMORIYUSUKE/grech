from typing import List
from pydantic import BaseModel


# コマンド実行結果
class ReadTestInfo(BaseModel):
    name: str  