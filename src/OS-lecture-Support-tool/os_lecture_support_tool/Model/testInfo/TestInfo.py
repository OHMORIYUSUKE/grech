from typing import Optional
from pydantic import BaseModel


# テストの情報
class TestInfo(BaseModel):
    name: Optional[str]
    description: Optional[str]
    docs_url: Optional[str]
    author: Optional[str]
    copyright: Optional[str]
