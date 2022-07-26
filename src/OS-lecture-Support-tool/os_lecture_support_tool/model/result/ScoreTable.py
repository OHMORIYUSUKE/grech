from typing import List
from pydantic import BaseModel


class Row(BaseModel):
    chapter: str
    name: List[str]
    score: int
    max_score: int


# スコア結果
class ScoreTable(BaseModel):
    result: List[Row]
