from fastapi import APIRouter, Depends, HTTPException, status
from .user_model import User
from datetime import datetime, timedelta, timezone
from typing import Annotated
from sqlalchemy.orm import Session

import sys
sys.path.append('..')
from database import init_db
from .user_vo import UserRequest, Token, RefreshTokenRequest
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError

user_route = APIRouter()

SECRET_KEY = ''
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'])
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/login')

db_dependency = Annotated[Session, Depends(init_db)]

@user_route.post('/register', status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserRequest, db: db_dependency):
    new_user = User(
        username = user_data.username,
        email = user_data.email,
        password = bcrypt_context.hash(user_data.password)
    )

    db.add(new_user)
    db.commit()

@user_route.post('/login')
def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                     db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='could not validate user.'
        )
    
    token = create_access_token(user.username, user.user_id)
    refresh_token = create_refresh_token(user.username, user.user_id)

    return {'access_token': token, 'refresh_token': refresh_token, 'token_type': 'bearer'}

def authenticate_user(username, password, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user

def create_access_token(username, user_id):
    return create_token(username, user_id, timedelta(1))

def create_refresh_token(username, user_id):
    return create_token(username, user_id, timedelta(1))

def create_token(username, user_id, expires_delta):
    encode = {'sub': username, 'user_id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

@user_route.post('/refresh', response_model=Token)
def refresh_token(refresh_token_request: RefreshTokenRequest):
    try:
        payload = jwt.decode(refresh_token_request.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        user_id = payload.get('user_id')
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid refresh token.'
            )

        access_token = create_access_token(username, user_id)

        return {
            'access_token': access_token,
            'token_type': 'bearer'
        }
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Refresh token has expired.'
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid refresh token.'
        )

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        user_id = payload.get('user_id')
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='could not validate user.'
            )
        return {'username': username, 'user_id': user_id}
    
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token has expired.'
        )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='could not validate user.'
        )