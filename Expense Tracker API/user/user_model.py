from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship

import sys
sys.path.append('..')
from database import Base

from expense.expense_model import Expense

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(256), nullable=False)

    expenses = relationship("Expense", back_populates='user', cascade='all, delete')