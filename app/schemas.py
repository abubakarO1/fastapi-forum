from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True   # ✅ Pydantic v2 (replaces orm_mode)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


class ThreadCreate(BaseModel):
    title: str
    content: str

class ThreadResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    owner: UserResponse   # ✅ include user info

    class Config:
        from_attributes = True


class PostCreate(BaseModel):
    content: str

class PostResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    updated_at: datetime
    author: UserResponse   # ✅ include user info

    class Config:
        from_attributes = True


class CommentCreate(BaseModel):
    content: str

class CommentResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    updated_at: datetime
    author: UserResponse   # ✅ include user info

    class Config:
        from_attributes = True
