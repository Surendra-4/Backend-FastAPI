"""
post.py contains routes associated with posts.
"""

from fastapi import Depends, HTTPException, status, Response, APIRouter
from sqlalchemy.orm import Session
from typing import List
from pydantic import EmailStr

from .. import schemas, models, oauth2
from .. database import get_db

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

# Path Operation Functions of "Posts"

# Route dedicated to creating posts
@router.post("/", response_model=schemas.PostResponse)
def create_post(post: schemas.PostBase, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id = current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Route dedicated to getting posts
@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    return posts


@router.get("/", response_model=schemas.PostResponse)
def get_user_posts(email: EmailStr, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    """
    Reminder: Please fix this function
    """
    db.query(models.User)

# Route dedicated to getting the latest post
@router.get("/latest", response_model=schemas.PostResponse)
def get_latest(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
    return post

# Route dedicated to getting a post based on a ID
@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    return post

# Route dedicated to updating a post based on a ID
@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostBase, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    updated = post_query.first()
    
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    
    return updated
    
# Route dedicated to deleting a post based on a ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    
    post.delete(synchronize_session=False)
    db.commit()
    
    return post