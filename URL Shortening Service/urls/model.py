from sqlalchemy import String, Integer, Column, DateTime
from datetime import datetime
import sys
sys.path.append('..')
from database import Base

class Url(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(100), unique=True, nullable=False)
    shortcode = Column(String(100), unique=True, nullable=False)
    createdAt = Column(DateTime, default=datetime.now())
    updatedAt = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    accessCount = Column(Integer, default=0, onupdate=0)