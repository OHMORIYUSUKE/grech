from typing import List
from pydantic import BaseModel


class TestInfo(BaseModel):
    name: str
