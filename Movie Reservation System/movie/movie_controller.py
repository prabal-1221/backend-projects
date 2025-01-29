from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session
import sys
sys.path.append("..")
from database import init_db
from .movie_model import Genre, Movie, MovieGenre
from .movie_vo import MovieRequest
sys.path.append("..")
from user.user_controller import get_current_user

movie_route = APIRouter(prefix = "/movies")

db_dependency = Annotated[Session, Depends(init_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

def get_all_genres(db: db_dependency):
    genres = db.query(Genre).all()

    return genres

@movie_route.post("/")
def add_movie(movie_data: MovieRequest, db: db_dependency, user: user_dependency):
    if not user or user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you are not authorized.")

    new_movie = Movie(
        title = movie_data.title,
        description = movie_data.description,
        poster = movie_data.poster
    )

    db.add(new_movie)
    db.flush()

    genres = get_all_genres(db)
    genre_dict = {genre.genre_name: genre.genre_id for genre in genres}

    movie_genre_objects = [MovieGenre(movie_id=new_movie.movie_id, genre_id=genre_dict[genre]) for genre in movie_data.genres]

    db.bulk_save_objects(movie_genre_objects)
    
    db.commit()
    db.refresh(new_movie)

    return new_movie

@movie_route.get("/{movie_id}")
def get_movie(movie_id: int, db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you are not authorized.")

    movie = db.query(Movie).filter(Movie.movie_id == movie_id).first()

    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="movie not found.")
    
    return movie

@movie_route.get("/{movie_id}/genres")
def get_movie_genres(movie_id: int, db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you are not authorized.")

    genres = (
        db.query(Genre)
        .join(MovieGenre, Genre.genre_id == MovieGenre.genre_id)
        .filter(MovieGenre.movie_id == movie_id)
        .all()
    )

    return genres


@movie_route.put("/{movie_id}")
def update_movie(movie_id: int, movie_data: MovieRequest, db: db_dependency, user: user_dependency):
    if not user or user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you are not authorized.")

    movie = db.query(Movie).filter(Movie.movie_id == movie_id).first()

    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="movie not found.")
    
    movie.title = movie_data.title
    movie.description = movie_data.description
    movie.poster = movie_data.poster

    db.query(MovieGenre).filter(MovieGenre.movie_id == movie_id).delete(synchronize_session="fetch")
    
    genres = get_all_genres(db)
    genre_dict = {genre.genre_name: genre.genre_id for genre in genres}
    
    new_genres = [MovieGenre(movie_id=movie.movie_id, genre_id=genre_dict[genre]) for genre in movie_data.genres]
    db.bulk_save_objects(new_genres)
    
    db.commit()
    db.refresh(movie)

    return movie

@movie_route.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int, db: db_dependency, user: user_dependency):
    if not user or user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you are not authorized.")

    movie = db.query(Movie).filter(Movie.movie_id == movie_id).one_or_none()

    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="movie not found.")

    db.query(MovieGenre).filter(MovieGenre.movie_id == movie_id).delete(synchronize_session="fetch")
    db.delete(movie)
    
    db.commit()

@movie_route.get("/{genre}")
def get_movies_by_genre(genre: str, db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized.")
    
    genre_db = db.query(Genre).filter(Genre.genre_name == genre).first()
    if not genre_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found.")
    
    movies = (
        db.query(Movie)
        .join(MovieGenre, Movie.movie_id == MovieGenre.movie_id)
        .filter(MovieGenre.genre_id == genre_db.genre_id)
        .all()
    )

    return movies


