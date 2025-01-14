from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from urllib.parse import quote_plus

Base = declarative_base()

password = "Sql@1234"
encoded_password = quote_plus(password)
DATABASE_URL = f'mysql+pymysql://root:{encoded_password}@localhost:3306/blogapplication'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def create_db():
    Base.metadata.create_all(bind=engine)

def init_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()