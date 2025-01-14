from vo import BlogRequest
from model import Blogs
from sqlalchemy.orm import Session

class BlogDao:
    def create_post(blog_data: BlogRequest, db: Session):
        new_post = Blogs(
            title = blog_data.title,
            content = blog_data.content,
            category = blog_data.category,
            tags = blog_data.tags,
        )
        db.add(new_post)
        db.commit()
        db.refresh(new_post)

        return new_post
    
    def update_post(post_id: int, blog_data: BlogRequest, db: Session):
        post = db.query(Blogs).filter(Blogs.id == post_id).first()

        if not post:
            return None
        
        post.title = blog_data.title
        post.content = blog_data.content
        post.category = blog_data.category
        post.tags = blog_data.tags

        db.commit()
        db.refresh(post)

        return post
    
    def delete_post(post_id: int, db: Session):
        post = db.query(Blogs).filter(Blogs.id == post_id).first()

        if not post:
            return None
        
        db.delete(post)
        db.commit()

        return post

    def get_post(post_id: int, db: Session):
        return db.query(Blogs).filter(Blogs.id == post_id).first()

    def get_all_post(db: Session):
        return db.query(Blogs).all()

    def get_term_post(term: str, db: Session):
        return db.query(Blogs).filter(Blogs.tags.contains(term)).all()

