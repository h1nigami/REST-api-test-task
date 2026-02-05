from pydantic import BaseModel
from typing import List

class PaginationParams(BaseModel):
    skip: int = 0
    limit: int = 100

class ListResponse(BaseModel):
    items: List[dict]
    total: int
    skip: int
    limit: int