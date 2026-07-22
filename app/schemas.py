"""
This file contains tailored schemas for handling both input and output
associated with posts, users and authentication.
"""

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# The following classes deal with schema associated with 'User'        
class UserCreate(BaseModel):
    email : EmailStr
    password: str
    
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        from_attributes = True


# The following class deals with schema associated with 'Authentication'
class AuthBase(BaseModel):
    email: EmailStr
    password: str
    
    
# The following class deals with schema associated with 'JWT Tokens'

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    email: Optional[str] = None


# The following classes deal with schema associated with 'Post'
class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True
    
class Post(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    
    class Config:
        from_attributes = True
