from sqlalchemy.orm import Session
import sys
sys.path.append('..')
from database import init_db
from typing import Annotated
from fastapi import Depends
from movie_model import Genre

def seed_genres(db: Annotated[Session, Depends(init_db)]):
    genres = ["Action", "Comedy", "Drama", "Horror", "Romance", "Sci-Fi", "Thriller", "Fantasy", "Documentary", "Adventure", "Animation", "Crime", "Mystery", "Historical", "Musical", "Western"]

    for genre in genres:
        pass