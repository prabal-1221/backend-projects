from sqlalchemy import Column, Integer, String, ForeignKey
import sys
sys.path.append('..')
from database import Base
from sqlalchemy.orm import relationship

class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    poster = Column(String(100), nullable=False)

    genres = relationship("Genre", secondary="movies_genres", back_populates="movies")

class Genre(Base):
    __tablename__ = "genres"

    genre_id = Column(Integer, primary_key=True, index=True)
    genre_name = Column(String(50), nullable=False)

    movies = relationship("Movie", secondary="movies_genres", back_populates="genres")

class MovieGenre(Base):
    __tablename__ = "movies_genres"

    movie_id = Column(Integer, ForeignKey("movies.movie_id"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genres.genre_id"), primary_key=True)