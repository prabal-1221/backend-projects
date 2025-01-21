from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from urllib.parse import quote_plus

Base = declarative_base()

encoded_password = quote_plus("Sql@1234")
DATABASE_URL = f'mysql+pymysql://root:{encoded_password}@localhost:3306/ecommerceapplication'

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
