from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
import sys
sys.path.append('..')
from database import Base
sys.path.append('..')
from datetime import datetime
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(256), nullable=False)
    createdAt = Column(DateTime, default=datetime.now)
    updatedAt = Column(DateTime, default=datetime.now,  onupdate=datetime.now)
    
    cart = relationship("Cart", back_populates='user', uselist=False, cascade='all, delete')