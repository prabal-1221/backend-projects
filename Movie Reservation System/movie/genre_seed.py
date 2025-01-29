import sys
sys.path.append('..')
from database import SessionLocal
from .movie_model import Genre

def seed_genres():
    db = SessionLocal()
    try:
        genres = ["Action", "Comedy", "Drama", "Horror", "Romance", "Sci-Fi", "Thriller", "Fantasy", "Documentary", "Adventure", "Animation", "Crime", "Mystery", "Historical", "Musical", "Western"]

        for genre in genres:
            genre_name = db.query(Genre).filter(Genre.genre_name == genre).first()

            if not genre_name:
                db.add(Genre(genre_name = genre))

        db.commit()
    
    finally:
        db.close()