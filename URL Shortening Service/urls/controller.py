from fastapi import APIRouter, Depends, status, HTTPException
from .vo import UrlRequest, UrlResponse_1, UrlResponse_2
import sys
sys.path.append('..')
from database import init_db
from typing import Annotated
from sqlalchemy.orm import Session
from .model import Url
import secrets
import string

url_route = APIRouter(prefix="/shorten")

db_dependency = Annotated[Session, Depends(init_db)]

def create_shortcode(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

@url_route.post("/", status_code=status.HTTP_201_CREATED)
def create_shorten_url(url_data: UrlRequest, db: db_dependency):
    generated_shortcode = create_shortcode()

    new_url = Url(
        url = url_data.url,
        shortcode = generated_shortcode,
    )

    db.add(new_url)
    db.commit()

@url_route.get("/{shortcode}", response_model=UrlResponse_1)
def get_shorten_url(shortcode: str, db: db_dependency):
    url = db.query(Url).filter(Url.shortcode == shortcode).first()

    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no url found.')
    
    url.accessCount += 1

    db.commit()
    db.refresh(url)
    
    return url

@url_route.put("/{shortcode}", response_model=UrlResponse_1)
def update_shorten_url(shortcode: str, url_data: UrlRequest, db: db_dependency):
    url = db.query(Url).filter(Url.shortcode == shortcode).first()

    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no url found.')
    
    url.url = url_data.url

    db.commit()
    db.refresh(url)

    return url

@url_route.delete("/{shortcode}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shorten_url(shortcode: str, db: db_dependency):
    url = db.query(Url).filter(Url.shortcode == shortcode).first()

    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no url found.')
    
    db.delete(url)
    db.commit()
    
@url_route.get("/{shortcode}/stats", response_model=UrlResponse_2)
def get_shorten_url_stats(shortcode: str, db: db_dependency):
    url = db.query(Url).filter(Url.shortcode == shortcode).first()

    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no url found.')
    
    return url