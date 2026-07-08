from fastapi import FastAPI, Depends
from random import randrange
from typing import Optional, List
from fastapi import Response, status, HTTPException

import psycopg
from psycopg.rows import dict_row
import time

from . import models, schemas
from .database import Base, engine, get_db
from sqlalchemy.orm import Session
from .utils import hash_password

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
    
while True:
    try:
        conn = psycopg.connect(dbname="fastapi", user="postgres", password="56785678", host="localhost", row_factory=dict_row)
        cursor = conn.cursor()
        print("Database connection is successfully established!")
        break
    
    except Exception as error:
        print("Database connection was not established")
        print(error)
        time.sleep(2)


### Path Operation Functions of "Posts"

@app.post("/posts", response_model=schemas.PostResponse)
def create_post(post: schemas.PostBase, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.get("/posts/latest", response_model=schemas.PostResponse)
def get_latest(db: Session = Depends(get_db)):
    post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
    return post


@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    return post


@app.put("/posts/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostBase, db: Session = Depends(get_db)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    updated = post_query.first()
    
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    
    return updated
    

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    
    post.delete(synchronize_session=False)
    db.commit()
    
    return post

### Path Operation Functions of "Users"

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    user.password = hash_password(user.password)
    
    new_user = models.User(**user.model_dump())
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@app.get("/users/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id: {id} not found')
    
    return user