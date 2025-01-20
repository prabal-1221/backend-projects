"""
Create a new short URL
Retrieve an original URL from a short URL
Update an existing short URL
Delete an existing short URL
Get statistics on the short URL (e.g., number of times accessed)
"""

from fastapi import FastAPI
from database import create_db
from urls.controller import url_route

create_db()

app = FastAPI()
app.include_router(url_route)

@app.get("/")
def index():
    return {"message": "server is running."}