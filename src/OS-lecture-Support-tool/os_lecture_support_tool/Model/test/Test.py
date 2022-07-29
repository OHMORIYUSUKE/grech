from typing import List
from pydantic import BaseModel


class Regexp(BaseModel):
    type: str
    list: List[str]


# テスト１つ
class Test(BaseModel):
    name: str
    cmd: str
    working_directory: str
    regexp: Regexp
    message: str
