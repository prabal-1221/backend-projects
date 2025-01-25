from pydantic import BaseModel
from typing import Literal

class ExerciseRequest(BaseModel):
    exercise_name: str
    exercise_description: str
    exercise_category: Literal["cardio", "strength", "flexibility", "balance", "power", "endurance"]
    exercise_muscle_group: Literal["chest", "back", "shoulders", "arms", "core", "legs", "glutes", "calves", "full-body"]
