from fastapi import APIRouter, Depends, HTTPException, status
import sys
sys.path.append('..')
from database import init_db
from sqlalchemy.orm import Session
from typing import Annotated
from .product_model import Product
from .product_vo import ProductRequest

product_route = APIRouter(prefix='/product')

db_dependency = Annotated[Session, Depends(init_db)]

@product_route.get('/', tags=["product"])
def get_products(db: db_dependency):
    products = db.query(Product).all()

    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no products found.')
    
    return products

@product_route.get('/{product_id}', tags=["product"])
def get_product_by_id(product_id: int, db: db_dependency):
    product = db.query(Product).filter(Product.product_id == product_id).first

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no product found.')
    
    return product

@product_route.post('/', status_code=status.HTTP_201_CREATED, tags=["product"])
def add_product(product_data: ProductRequest, db: db_dependency):
    new_product = Product(
        title = product_data.title,
        description = product_data.description,
        price = product_data.price
    )

    db.add(new_product)
    db.commit()

@product_route.put('/{product_id}', status_code=status.HTTP_200_OK, tags=["product"])
def update_product(product_id: int, product_data: ProductRequest, db: db_dependency):
    product = db.query(Product).filter(Product.product_id == product_id).first

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no product found.')
    
    product.title = product_data.title
    product.description = product_data.description
    product.price = product_data.price

    db.commit()

@product_route.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT, tags=["product"])
def delete_product(product_id: int, db: db_dependency):
    product = db.query(Product).filter(Product.product_id == product_id).first

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no product found.')
    
    db.delete(product)
    db.commit()

