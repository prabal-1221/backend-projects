from sqlalchemy import create_engine
from urllib.parse import quote_plus
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

password = 'Sql@1234'
encode_password = quote_plus(password)

DATABASE_URL = f'mysql+pymysql://root:{encode_password}@localhost:3306/workoutapplication'

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