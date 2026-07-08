from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True
    
class Post(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
        
class UserCreate(BaseModel):
    email : EmailStr
    password: str
    
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        from_attributes = True