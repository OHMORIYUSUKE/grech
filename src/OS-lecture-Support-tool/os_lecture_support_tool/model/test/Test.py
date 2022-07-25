from typing import List
from pydantic import BaseModel


# テスト１つ
class Regexp(BaseModel):
    type: str
    list: List[str]


class Test(BaseModel):
    name: str
    cmd: str
    working_directory: str
    regexp: Regexp
    message: str
