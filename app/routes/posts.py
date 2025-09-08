from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Post, Thread
import app.schemas as schemas
from app.routes.auth import get_current_user


router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/threads/{thread_id}", response_model=schemas.PostResponse)
def create_post(thread_id: int, post: schemas.PostCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    thread = db.query(Thread).filter(Thread.id == thread_id).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    new_post = Post(content=post.content, thread_id=thread_id, user_id=user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/threads/{thread_id}", response_model=list[schemas.PostResponse])
def get_posts(thread_id: int, db: Session = Depends(get_db)):
    return db.query(Post).filter(Post.thread_id == thread_id).all()

@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post_data: schemas.PostCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Not found")
    if post.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not your post")
    post.content = post_data.content
    db.commit()
    db.refresh(post)
    return post

@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Not found")
    if post.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not your post")
    db.delete(post)
    db.commit()
    return {"msg": "Post deleted"}
