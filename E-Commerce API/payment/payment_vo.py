from pydantic import BaseModel

class PaymentRequest(BaseModel):
    price: int
    email: str
