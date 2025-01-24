from passlib.context import CryptContext
from typing import Annotated
from fastapi import Depends, APIRouter, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import sys
sys.path.append('..')
from database import init_db
from sqlalchemy.orm import Session
from .user_vo import UserRequest
from .user_model import User
from datetime import datetime, timezone, timedelta
from jose import jwt
from jose.exceptions import ExpiredSignatureError
from cart.cart_model import Cart

SECRET_KEY = '064d60c7-899a-4c9b-bce7-d4f7670efb1f'
ALGORITHM = 'HS256'

bcrypt = CryptContext(schemes="bcrypt")
oath2_bearer = OAuth2PasswordBearer(tokenUrl='/login')

user_route = APIRouter()

db_dependency = Annotated[Session, Depends(init_db)]

@user_route.post("/register", status_code=status.HTTP_201_CREATED, tags=["user"])
def create_user(user_data: UserRequest, db: db_dependency):
    new_user = User(
        username = user_data.username,
        email = user_data.email,
        password = bcrypt.hash(user_data.password)
    )
    new_cart = Cart(user = new_user)

    db.add(new_user)
    db.add(new_cart)  # Add the new cart to the session
    db.commit()  # Commit both user and cart to the database


@user_route.post("/login", tags=["user"])
def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    username = form_data.username
    password = form_data.password

    user = authenticate_user(username, password, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated.")
    
    token = create_token(user)

    return {'access_token': token, 'token_type': 'bearer'}



def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()

    if not user or not bcrypt.verify(password, user.password):
        return False
    
    return user

def create_token(user, timeout: timedelta = timedelta(minutes=15)):
    encode = {'user_id': user.user_id, 'username': user.username}
    expiry = datetime.now(timezone.utc) + timeout
    encode.update({'exp': expiry})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: Annotated[str, Depends(oath2_bearer)], db: db_dependency):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get('user_id')
        username = payload.get('username')

        if not user_id or not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='user not authenticated.')
        
        user = db.query(User).filter(User.user_id == user_id).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='user not authenticated.')
        
        return {'user_id': user.user_id, 'username': user.username}
    
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='token has expired.')