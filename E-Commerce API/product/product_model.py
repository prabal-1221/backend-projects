from sqlalchemy import Column, Integer, String, DateTime
import sys
sys.path.append('..')
from database import Base
from datetime import datetime

class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=False)
    price = Column(Integer, nullable=False)
    updatedAt = Column(DateTime, default=datetime.now, onupdate=datetime.now)