from fastapi import FastAPI
from user import user_route
from admin import admin_route

app = FastAPI()

app.include_router(user_route)
app.include_router(admin_route)

@app.get('/')
def home():
    return {'message': 'server is running.'}