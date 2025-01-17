from fastapi import FastAPI, status, Depends, HTTPException
from database import create_db, init_db
from users.user_controller import user_route
from users.user_controller import get_current_user
from typing import Annotated
from sqlalchemy.orm import Session
from tasks.task_controller import task_route

app = FastAPI()
app.include_router(user_route)
app.include_router(task_route)

create_db()

user_dependency = Annotated[dict, Depends(get_current_user)]
db_dependency = Annotated[Session, Depends(init_db)]

@app.get('/', status_code=status.HTTP_200_OK)
def index(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Authentication Failed.'
        )
    return {'message': 'server is running'}