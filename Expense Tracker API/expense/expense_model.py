from sqlalchemy import String, Integer, Column, Float, ForeignKey, Date
from sqlalchemy.orm import relationship

import sys
sys.path.append('..')
from database import Base

class Expense(Base):
    __tablename__ = 'expenses'

    expense_id = Column(Integer, primary_key=True, index=True)
    category = Column(String(50), nullable=False)
    description = Column(String(100), nullable=False)
    amount = Column(Float(2), nullable=False)
    date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'))

    user = relationship("User", back_populates='expenses')