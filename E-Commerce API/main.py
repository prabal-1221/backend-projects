from fastapi import FastAPI, Depends, HTTPException, status
from user.user_controller import user_route, get_current_user
from typing import Annotated
from database import create_db
from product.product_controller import product_route
from cart.cart_controller import cart_route

create_db()

app = FastAPI()
app.include_router(user_route)
app.include_router(product_route)
app.include_router(cart_route)

user_dependency = Annotated[dict, Depends(get_current_user)]

@app.get("/")
def index(user: user_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='user not authenticated.')
    return {"message": "server is running."}