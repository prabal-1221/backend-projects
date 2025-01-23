from fastapi import APIRouter, HTTPException, status, Depends
from .payment_vo import PaymentRequest
from .payment_model import Payment
import stripe
import sys
sys.path.append('..')
from user.user_controller import get_current_user
from typing import Annotated
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session
sys.path.append('..')
from database import init_db
sys.path.append('..')
from cart.cart_model import Cart
sys.path.append('..')
from cart.cart_product_model import CartItem
sys.path.append('..')
from user.user_model import User

load_dotenv()

payment_route = APIRouter(prefix='/payment')

stripe.api_key = os.getenv('STRIPE_KEY')

user_dependency = Annotated[dict, Depends(get_current_user)]
db_dependency = Annotated[Session, Depends(init_db)]

@payment_route.post('/', tags=["payments"])
def process_payment(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='user not authenticated.')

    try:
        user_db = db.query(User).filter(User.user_id == user['user_id']).first()
        cart_id = user_db.cart.cart_id

        cart_item = db.query(CartItem).filter(CartItem.cart_id == cart_id).all()

        total_price = 0

        for item in cart_item:
            total_price += item.__dict__['price']*item.__dict__['quantity']

        intent = stripe.PaymentIntent.create(
            amount = total_price,
            currency='inr',
            receipt_email=user_db.email
        )

        client_secret = intent.client_secret
        payment_id = client_secret.split('_secret_')[0]

        payment_object = Payment(
            payment_id = payment_id,
            user_id = user_db.user_id,
            price = total_price,
            receipt_email = user_db.email,
        )

        db.query(CartItem).filter(CartItem.cart_id == cart_id).delete()

        db.add(payment_object)
        db.commit()
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))