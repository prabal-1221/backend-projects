from fastapi import APIRouter, Depends, HTTPException, status
import sys
sys.path.append('..')
from database import init_db
from sqlalchemy.orm import Session
from typing import Annotated
from .product_model import Product
from .product_vo import ProductRequest
from sqlalchemy import or_
sys.path.append('..')
from user.user_controller import get_current_user
sys.path.append('..')
from user.user_model import User
import os
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

bcrypt = CryptContext(schemes="bcrypt")

product_route = APIRouter(prefix='/product')

db_dependency = Annotated[Session, Depends(init_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

USERNAME = os.getenv('ADMIN_USERNAME')
PASSWORD = os.getenv('ADMIN_PASSWORD')

@product_route.get('/', tags=["product"])
def get_products(db: db_dependency):

    products = db.query(Product).all()

    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no products found.')
    
    return products

@product_route.get('/{product_id}', tags=["product"])
def get_product_by_id(product_id: int, user: user_dependency, db: db_dependency):

    product = db.query(Product).filter(Product.product_id == product_id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no product found.')
    
    return product

@product_route.post('/', status_code=status.HTTP_201_CREATED, tags=["product"])
def add_product(product_data: ProductRequest, user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='user not found.')
    
    user_db = db.query(User).filter(User.user_id == user['user_id']).first()

    if user_db.username != USERNAME or not bcrypt.verify(PASSWORD, user_db.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='only for admin.')

    new_product = Product(
        title = product_data.title,
        description = product_data.description,
        price = product_data.price
    )

    db.add(new_product)
    db.commit()

@product_route.put('/{product_id}', status_code=status.HTTP_200_OK, tags=["product"])
def update_product(product_id: int, product_data: ProductRequest, user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='user not found.')
    
    user_db = db.query(User).filter(User.user_id == user['user_id']).first()

    if user_db.username != USERNAME or not bcrypt.verify(PASSWORD, user_db.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='only for admin.')
    
    product = db.query(Product).filter(Product.product_id == product_id).first

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no product found.')
    
    product.title = product_data.title
    product.description = product_data.description
    product.price = product_data.price

    db.commit()

@product_route.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT, tags=["product"])
def delete_product(product_id: int, user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='user not found.')
    
    user_db = db.query(User).filter(User.user_id == user['user_id']).first()

    if user_db.username != USERNAME or not bcrypt.verify(PASSWORD, user_db.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='only for admin.')
    
    product = db.query(Product).filter(Product.product_id == product_id).first

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no product found.')
    
    db.delete(product)
    db.commit()

@product_route.get('/', tags=["product"])
def search_product(name: str, user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='user not found.')
    
    user_db = db.query(User).filter(User.user_id == user['user_id']).first()

    if user_db.username != USERNAME or not bcrypt.verify(PASSWORD, user_db.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='only for admin.')

    products = db.query(Product).all()

    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no products found.')
    
    search = f'%{name}%'

    similar_products = db.query(Product).filter(or_(Product.title.like(search), Product.description.like(search))).all()

    return similar_products