from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Comment, Post
import app.schemas as schemas
from app.routes.auth import get_current_user


router = APIRouter(prefix="/comments", tags=["Comments"])

@router.post("/posts/{post_id}", response_model=schemas.CommentResponse)
def create_comment(post_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    new_comment = Comment(content=comment.content, post_id=post_id, user_id=user.id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.get("/posts/{post_id}", response_model=list[schemas.CommentResponse])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    return db.query(Comment).filter(Comment.post_id == post_id).all()

@router.put("/{id}", response_model=schemas.CommentResponse)
def update_comment(id: int, comment_data: schemas.CommentCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    comment = db.query(Comment).filter(Comment.id == id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Not found")
    if comment.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not your comment")
    comment.content = comment_data.content
    db.commit()
    db.refresh(comment)
    return comment

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    comment = db.query(Comment).filter(Comment.id == id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    if comment.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your comment")
    db.delete(comment)
    db.commit()
    return 
