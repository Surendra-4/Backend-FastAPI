from fastapi import Depends, HTTPException, status, Response, APIRouter
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models
from .. database import get_db

router = APIRouter()

### Path Operation Functions of "Posts"

@router.post("/posts", response_model=schemas.PostResponse)
def create_post(post: schemas.PostBase, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.get("/posts/latest", response_model=schemas.PostResponse)
def get_latest(db: Session = Depends(get_db)):
    post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
    return post


@router.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    return post


@router.put("/posts/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostBase, db: Session = Depends(get_db)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    updated = post_query.first()
    
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    
    return updated
    

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    
    post.delete(synchronize_session=False)
    db.commit()
    
    return post