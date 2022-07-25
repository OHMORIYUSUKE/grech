from typing import List
from pydantic import BaseModel

from os_lecture_support_tool.model.test.Test import Test

# チャプターに存在する複数のテスト
class Chapter(BaseModel):
    name: str
    tests: List[Test]
