from typing import List
from pydantic import BaseModel

# YAMLファイルの名前
class TestInfo(BaseModel):
    name: str
