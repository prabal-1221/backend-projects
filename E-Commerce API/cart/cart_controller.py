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

cart_route = APIRouter(prefix='/cart/{user_id}')

db_dependency = Annotated[Session, Depends(init_db)]

@cart_route.get('/', tags=["cart"])
def get_cart(user_id: int, db: db_dependency):
    user = db.query(User).filter(User.user_id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found.')
    
    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == user.cart.cart_id,
    ).all()

    return cart_item

@cart_route.post('/{product_id}', status_code=status.HTTP_201_CREATED, tags=["cart"])
def add_to_cart(user_id: int, product_id: int, db: db_dependency):
    user = db.query(User).filter(User.user_id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found.')

    product = db.query(Product).filter(Product.product_id == product_id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='product not found.')
    
    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == user.cart.cart_id,
        CartItem.product_id == product_id
    ).first()

    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(cart_id=user.cart.cart_id, product_id=product_id, quantity=1)
        db.add(cart_item)

    db.commit()


@cart_route.delete('/{product_id}', tags=["cart"])
def delete_from_cart(user_id: int, product_id: int, db: db_dependency):
    user = db.query(User).filter(User.user_id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found.')

    product = db.query(Product).filter(Product.product_id == product_id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='product not found.')
    
    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == user.cart.cart_id,
        CartItem.product_id == product_id
    ).first()

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
    else:
        db.delete(cart_item)

    db.commit()

