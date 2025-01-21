from passlib.context import CryptContext
from typing import Annotated
from fastapi import Depends, APIRouter, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import sys
sys.path.append('..')
from database import init_db
from sqlalchemy.orm import Session
from .vo import UserRequest
from .model import User

SECRET_KEY = '064d60c7-899a-4c9b-bce7-d4f7670efb1f'
ALGORITHM = 'HS256'

bcrypt = CryptContext(schemes="bcrypt")
oath2_bearer = OAuth2PasswordBearer(tokenUrl='/login')

auth_route = APIRouter()

db_dependency = Annotated[Session, Depends(init_db)]

@auth_route.post("/register", status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserRequest, db: db_dependency):
    new_user = User(
        username = user_data.username,
        email = user_data.email,
        password = bcrypt.hash(user_data.password)
    )

    db.add(new_user)
    db.commit()

@auth_route.post("/login")
def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    username = form_data.username
    password = form_data.password

    user = authenticate_user(username, password, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not authenticated.")
    
    token = create_token(user)


def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()

    if not user or not bcrypt.verify(password, user.password):
        return False
    
    return user

def create_token():
    pass