from sqlalchemy import Column, Integer, DateTime, ForeignKey
import sys
sys.path.append('..')
from database import Base
sys.path.append('..')
from datetime import datetime
from sqlalchemy.orm import relationship

class Cart(Base):
    __tablename__ = 'carts'
    cart_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    user = relationship("User", back_populates='cart')
    items = relationship("CartItem", back_populates='cart')