from pydantic import BaseModel
from typing import Literal, List

class MovieRequest(BaseModel):
    title: str
    description: str
    poster: str
    genres: List[Literal["Action", "Comedy", "Drama", "Horror", "Romance", "Sci-Fi", "Thriller", "Fantasy", "Documentary", "Adventure", "Animation", "Crime", "Mystery", "Historical", "Musical"]]