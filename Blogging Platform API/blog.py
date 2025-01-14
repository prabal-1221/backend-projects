from fastapi import APIRouter, Depends, HTTPException, status, Query
from vo import BlogRequest, BlogResponse
from dao import BlogDao
from sqlalchemy.orm import Session
from database import init_db
from typing import List, Optional

blog_route = APIRouter(prefix='/blog')

@blog_route.post('/posts', response_model=BlogResponse, tags=["blogs"])
def create_post_controller(blog_data: BlogRequest, db: Session = Depends(init_db)):
    return BlogDao.create_post(blog_data, db)

@blog_route.put('/posts/{post_id}', response_model=BlogResponse, tags=["blogs"])
def update_post_controller(post_id: int, blog_data: BlogRequest, db: Session = Depends(init_db)):
    return BlogDao.update_post(post_id, blog_data, db)

@blog_route.delete('/posts/{post_id}', tags=["blogs"])
def delete_post_controller(post_id: int, db: Session = Depends(init_db)):
    post = BlogDao.delete_post(post_id, db)

    if post:
        return None
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found.')

@blog_route.get('/posts/{post_id}', response_model=BlogResponse, tags=["blogs"])
def get_post_controller(post_id: int, db: Session = Depends(init_db)):
    post = BlogDao.get_post(post_id, db)

    if post:
        return post
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found.')

@blog_route.get('/posts', response_model=List[BlogResponse], tags=["blogs"])
def get_all_post_controller(term: Optional[str] = Query(None, description='Search term for filtering posts'), db: Session = Depends(init_db)):
    post = []

    if term:
        post = BlogDao.get_term_post(term, db)
    else:
        post = BlogDao.get_all_post(db)

    if len(post):
        return post
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No posts in database.')

