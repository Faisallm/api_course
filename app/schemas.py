from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, Annotated


class PostBase(BaseModel):
    title: str
    content: str 
    # default value of True
    published: bool = True


class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class Post(PostBase):
    id: int
    created_at: datetime
    # owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    post: Post
    votes: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(UserCreate):
    pass

# schema for the token
class Token(BaseModel):
    access_token: str
    token_type: str

# schema for token payload
class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    # less than or equal to 1 constraint
    dir: Annotated[int, Field(gt=-1, le=1)]