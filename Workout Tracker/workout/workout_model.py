from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Boolean, Float
import sys
sys.path.append('..')
from database import Base
from datetime import datetime

class Workout(Base):
    __tablename__ = "workouts"

    workout_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    workout_name = Column(String(50), nullable=False)
    workout_description = Column(String(200), nullable=False)
    workout_scheduled_date = Column(Date, nullable=False)
    workout_completed = Column(Boolean, default=False)
    workout_completed_date = Column(Date, default=None)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class WorkoutExercise(Base):
    __tablename__ = "workout_exercise"

    workout_exercise_id = Column(Integer, primary_key=True, index=True)
    Workout_id = Column(Integer, ForeignKey("workouts.workout_id"))
    exercise_id = Column(Integer, ForeignKey("exercises.exercise_id"))
    sets = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    weight = Column(Float, default=None)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)