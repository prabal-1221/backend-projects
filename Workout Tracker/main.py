from fastapi import FastAPI, Depends, HTTPException, status
from database import create_db
from user.user_controller import user_route, get_current_user
from typing import Annotated

create_db()

app = FastAPI()
app.include_router(user_route)

user_dependency = Annotated[dict, Depends(get_current_user)]

@app.get("/")
def home(user: user_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not authenticated.")
    return {"message": "server is running."}