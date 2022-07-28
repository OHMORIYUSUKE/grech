from typing import List
from pydantic import BaseModel


# 設定
class UserConfig(BaseModel):
    name: str
    value: str


class UserConfigList(BaseModel):
    list: List[UserConfig]
