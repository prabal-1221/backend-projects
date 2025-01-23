from sqlalchemy import Column, Integer, String, DateTime
import sys
sys.path.append('..')
from database import Base
sys.path.append('..')
from datetime import datetime

class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(String(100), primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    receipt_email = Column(String(100), nullable=False)
    createdAt = Column(DateTime, default=datetime.now)