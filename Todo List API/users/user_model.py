from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship
import sys
sys.path.append('..')
from database import Base

sys.path.append('..')
from tasks.task_model import Task

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255))

    tasks = relationship('Task', back_populates='user', cascade='all, delete')