from fastapi import FastAPI
from database import create_db
from blog import blog_route

create_db()

app = FastAPI()

app.include_router(blog_route)

@app.get('/')
def home():
    return {'message': 'server is running.'}