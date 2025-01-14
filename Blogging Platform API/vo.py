from pydantic import BaseModel
from typing import List
from datetime import datetime

class BlogRequest(BaseModel):
    title: str
    content: str
    category: str
    tags: List[str]

class BlogResponse(BaseModel):
    id: int
    title: str
    content: str
    category: str
    tags: List[str]
    createdAt: datetime
    updatedAt: datetime