from pydantic import BaseModel
from typing import Literal
from datetime import date

class ExpenseRequest(BaseModel):
    category: Literal["Groceries", "Leisure", "Electronics", "Utilities", "Clothing", "Health", "Others"]
    description: str
    amount: float
    date: date