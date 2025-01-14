from sqlalchemy import Integer, String, Column, DateTime, JSON
from datetime import datetime
from database import Base

class Blogs(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    content = Column(String(500), nullable=False)
    category = Column(String(50), nullable=False)
    tags = Column(JSON, nullable=False)
    createdAt = Column(DateTime, nullable=False, default=datetime.now())
    updatedAt = Column(DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())
