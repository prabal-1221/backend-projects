from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, status, HTTPException
from .user_vo import UserRequest
from typing import Annotated
from sqlalchemy.orm import Session
import sys
sys.path.append("..")
from database import init_db
from .user_model import User
from datetime import datetime, timedelta
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError

SECRET_KEY = "f06bdbd6-4f9f-43bc-bdb8-758502bc4f2a"
ALGORITHM = "HS256"

bcrypt = CryptContext(schemes=["bcrypt"])
oath2_bearer = OAuth2PasswordBearer(tokenUrl="/login")

user_route = APIRouter()

db_dependency = Annotated[Session, Depends(init_db)]

@user_route.post("/register", status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserRequest, db: db_dependency):
    user_db = User(
        username = user_data.username,
        email = user_data.email,
        password = bcrypt.hash(user_data.password)
    )

    db.add(user_db)
    db.commit()

@user_route.post("/login")
def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    username = form_data.username
    password = form_data.password

    user_db = authenticate_user(username, password, db)

    if not user_db:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not authenticated.")
    
    token = create_token(user_db)

    return {"access_token": token, "token_type": "bearer"}

def authenticate_user(username: str, password: str, db: Session):
    user_db = db.query(User).filter(User.username == username).first()

    if (not user_db) or (not bcrypt.verify(password, user_db.password)):
        return False
    
    return user_db

def create_token(user_db):
    encode = {"user_id": user_db.user_id, "username": user_db.username}
    expiry = datetime.now() + timedelta(minutes=20)
    encode.update({"exp": expiry})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: Annotated[str, Depends(oath2_bearer)], db: db_dependency):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload["user_id"]
        username = payload["username"]

        user_db = db.query(User).filter(User.user_id == user_id).first()

        if not user_db:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not authenticated.")
        
        return {"user_id": user_id, "username": username}
    
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not authenticated.")
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="something went wrong.")
