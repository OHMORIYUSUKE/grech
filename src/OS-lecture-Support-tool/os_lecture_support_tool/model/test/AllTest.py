from typing import List
from pydantic import BaseModel

from os_lecture_support_tool.model.test.Chapter import Chapter

# チャプターに存在する複数のテスト
class Alltest(BaseModel):
    all_test: List[Chapter]
