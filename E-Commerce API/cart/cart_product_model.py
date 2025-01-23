from sqlalchemy import Column, Integer, DateTime, ForeignKey
import sys
sys.path.append('..')
from database import Base
sys.path.append('..')
from datetime import datetime
from sqlalchemy.orm import relationship

class CartItem(Base):
    __tablename__ = 'cart_product'
    cart_id = Column(Integer, ForeignKey('carts.cart_id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), primary_key=True)
    quantity = Column(Integer, default=1)
    price = Column(Integer, nullable=False)
    updatedAt = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    cart = relationship("Cart", back_populates='items')
    product = relationship("Product")