from typing import List
from pydantic import BaseModel


class ScoreRow(BaseModel):
    chapter: str
    name: List[str]
    score: int
    max_score: int


# スコア結果
class ScoreTable(BaseModel):
    result: List[ScoreRow]
    status: bool  # すべてのテストを通過したか
