from pydantic import BaseModel

class ProductRequest(BaseModel):
    title: str
    description: str
    price: int