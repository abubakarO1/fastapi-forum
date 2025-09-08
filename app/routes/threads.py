from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models import Post, Thread
import app.schemas as schemas
from app.routes.auth import get_current_user


router = APIRouter(prefix="/threads", tags=["Threads"])

@router.post("/", response_model=schemas.ThreadResponse)
def create_thread(thread: schemas.ThreadCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    new_thread = Thread(title=thread.title, content=thread.content, user_id=user.id)
    db.add(new_thread)
    db.commit()
    db.refresh(new_thread)
    return new_thread

@router.get("/", response_model=list[schemas.ThreadResponse])
def list_threads(db: Session = Depends(get_db)):
    return db.query(Thread).all()

@router.get("/{id}", response_model=schemas.ThreadResponse)
def get_thread(id: int, db: Session = Depends(get_db)):
    thread = db.query(Thread).filter(Thread.id == id).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    return thread

@router.put("/{id}", response_model=schemas.ThreadResponse)
def update_thread(id: int, thread_data: schemas.ThreadCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    thread = db.query(Thread).filter(Thread.id == id).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Not found")
    if thread.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not your thread")
    thread.title = thread_data.title
    thread.content = thread_data.content
    db.commit()
    db.refresh(thread)
    return thread

@router.delete("/{id}")
def delete_thread(id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    thread = db.query(Thread).filter(Thread.id == id).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Not found")
    if thread.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not your thread")
    db.delete(thread)
    db.commit()
    return {"msg": "Thread deleted"}

# JOIN version: Thread + Posts + Comments
@router.get("/{id}/full")
def get_thread_full(id: int, db: Session = Depends(get_db)):
    thread = (
        db.query(Thread)
        .options(joinedload(Thread.posts).joinedload(Post.comments))
        .filter(Thread.id == id)
        .first()
    )
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")

    return {
        "id": thread.id,
        "title": thread.title,
        "content": thread.content,
        "posts": [
            {
                "id": post.id,
                "content": post.content,
                "comments": [
                    {"id": c.id, "content": c.content} for c in post.comments
                ]
            }
            for post in thread.posts
        ]
    }
