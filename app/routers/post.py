"""
post.py contains routes associated with posts.
"""

from fastapi import Depends, HTTPException, status, Response, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
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
def create_post(post: schemas.PostBase, db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id = current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Route dedicated to getting all posts
@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user),
            search: Optional[str] = '', limit: int = 5, skip: int = 0):
    
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

# Route dedicated to getting the all posts of the currently logged in user
@router.get("/user", response_model=List[schemas.PostResponse])
def get_user_posts(db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):
    user_posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return user_posts

# Route dedicated to getting the latest post of the currently logged in user
@router.get("/latest", response_model=schemas.PostResponse)
def get_latest(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.owner_id == current_user.id).order_by(
        models.Post.created_at.desc()).first()
    return post

# Route dedicated to getting a post based on a ID
@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    return post

# Route dedicated to updating a post based on a ID
@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostBase, db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    to_update = post_query.first()
    
    if to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    
    if to_update.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not authorized to perform the requested operation')
    
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    
    return post_query.first()
    
# Route dedicated to deleting a post based on a ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not authorized to perform the requested operation')
    
    db.delete(post)
    db.commit()
    return post