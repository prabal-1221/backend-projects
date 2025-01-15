from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship
import sys
sys.path.append('..')
from database import Base

class Task(Base):
    __tablename__ = 'tasks'

    task_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'))

    user = relationship("User", back_populates='tasks')