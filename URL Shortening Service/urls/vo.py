from pydantic import BaseModel
from datetime import datetime

class UrlRequest(BaseModel):
    url: str

class UrlResponse_1(BaseModel):
    id: int
    url: str
    shortcode: str
    createdAt: datetime
    updatedAt: datetime

class UrlResponse_2(BaseModel):
    id: int
    url: str
    shortcode: str
    createdAt: datetime
    updatedAt: datetime
    accessCount: int