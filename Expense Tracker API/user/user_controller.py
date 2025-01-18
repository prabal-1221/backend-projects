from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from database import init_db
from sqlalchemy.orm import Session
from user.user_vo import UserRequst, Token
from user.user_model import User
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError

SECRET_KEY = '257028ad-5326-4879-8d0e-ecd25b8ae4b6'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'])
oath2_bearer = OAuth2PasswordBearer(tokenUrl='/login')

user_route = APIRouter()

db_dependency = Annotated[Session, Depends(init_db)]

@user_route.post('/register', status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserRequst, db: db_dependency):
    new_user = User(
        username = user_data.username,
        email = user_data.email,
        password = bcrypt_context.hash(user_data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)


@user_route.post('/login', response_model=Token)
def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found.')
    
    access_token = create_access_token(user.username, user.user_id)

    return {'access_token': access_token, 'token_type': 'bearer'}

def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()

    if (not user) or (not bcrypt_context.verify(password, user.password)):
        return False
    
    return user

def create_access_token(username, user_id):
    return create_token(username, user_id, timedelta(minutes=5))

def create_token(username, user_id, expires_delta):
    encode = {'sub': username, 'user_id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: Annotated[str, Depends(oath2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        user_id = payload.get('user_id')

        if (not username) or (not user_id):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='user not authenticated.')
        
        return {'username': username, 'user_id': user_id}
    
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='token has expired.')
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='user not authenticated.')