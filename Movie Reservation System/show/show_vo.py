from pydantic import BaseModel
from datetime import datetime
from typing import List

class ShowRequest(BaseModel):
    show_time: datetime

class SeatRequest(BaseModel):
    seat_number: List[int]