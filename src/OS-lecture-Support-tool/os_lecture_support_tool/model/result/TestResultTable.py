from typing import List
from pydantic import BaseModel


class TestResultRow(BaseModel):
    chapter: str
    name: str
    cmd: str
    message: str
    status: int


# 結果
class TestResultTable(BaseModel):
    result: List[TestResultRow]
