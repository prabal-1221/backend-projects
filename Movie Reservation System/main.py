from fastapi import FastAPI, Depends, HTTPException, status
from database import create_db
from user.user_controller import user_route, get_current_user
from typing import Annotated
from movie.genre_seed import seed_genres
from movie.movie_controller import movie_route

create_db()
seed_genres()

app = FastAPI()
app.include_router(user_route)
app.include_router(movie_route)

user_dependency = Annotated[dict, Depends(get_current_user)]

@app.get("/")
def index(user: user_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not authenticated.")
    
    return {"message": "server is running."}