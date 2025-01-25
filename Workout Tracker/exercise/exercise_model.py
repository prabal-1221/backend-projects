from sqlalchemy import Column, Integer, String, DateTime
import sys
sys.path.append('..')
from database import Base
from datetime import datetime

class Exercise(Base):
    __tablename__ = "exercises"

    exercise_id = Column(Integer, primary_key=True, index=True)
    exercise_name = Column(String(50), unique=True, nullable=False)
    exercise_description = Column(String(200), unique=True, nullable=False)
    exercise_category = Column(String(20), nullable=False)
    exercise_muscle_group = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)