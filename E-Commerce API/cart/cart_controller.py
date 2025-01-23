from fastapi import APIRouter, Depends, HTTPException, status
import sys
sys.path.append('..')
from database import init_db
from typing import Annotated
from sqlalchemy.orm import Session
sys.path.append('..')
from user.user_model import User
sys.path.append('..')
from product.product_model import Product
from .cart_product_model import CartItem
sys.path.append('..')
from user.user_controller import get_current_user

cart_route = APIRouter(prefix='/cart')

db_dependency = Annotated[Session, Depends(init_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@cart_route.get('/', tags=["cart"])
def get_cart(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not authenticated.')
    
    user_db = db.query(User).filter(User.user_id == user['user_id']).first()
    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == user_db.cart.cart_id,
    ).all()

    return cart_item

@cart_route.post('/{product_id}', status_code=status.HTTP_201_CREATED, tags=["cart"])
def add_to_cart(product_id: int, user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not authenticated.')
    
    user_db = db.query(User).filter(User.user_id == user['user_id']).first()
    product = db.query(Product).filter(Product.product_id == product_id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='product not found.')
    
    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == user_db.cart.cart_id,
        CartItem.product_id == product_id
    ).first()

    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(cart_id=user_db.cart.cart_id, product_id=product_id, quantity=1, price=product.price)
        db.add(cart_item)

    db.commit()


@cart_route.delete('/{product_id}', tags=["cart"])
def delete_from_cart(user: user_dependency, product_id: int, db: db_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not authenticated.')
    
    user_db = db.query(User).filter(User.user_id == user['user_id']).first()


    product = db.query(Product).filter(Product.product_id == product_id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='product not found.')
    
    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == user_db.cart.cart_id,
        CartItem.product_id == product_id
    ).first()

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
    else:
        db.delete(cart_item)

    db.commit()

