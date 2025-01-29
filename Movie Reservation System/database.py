from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

DATABASE_URL = "sqlite:///./sample.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def create_db():
    Base.metadata.create_all(bind=engine)

def init_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()