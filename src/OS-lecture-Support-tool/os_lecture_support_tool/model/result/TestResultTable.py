from typing import List
from pydantic import BaseModel


class Row(BaseModel):
    chapter: str
    name: str
    cmd: str
    message: str


# 結果
class TestResultTable(BaseModel):
    result: List[Row]
