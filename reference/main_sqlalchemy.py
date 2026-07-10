from fastapi import FastAPI, Depends
from random import randrange
from pydantic import BaseModel
from typing import Optional
from fastapi import Response, status, HTTPException
import psycopg
from psycopg.rows import dict_row
import time
import models
from database import Base, engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool
    
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

    
my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favorite food", "content": "i like pizza", "id": 2}
]


@app.post("/posts")
def create_post(post: Post, db: Session = Depends(get_db())):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"new_post": new_post}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db())):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/posts/latest")
def get_latest(db: Session = Depends(get_db())):
    post = my_posts[len(my_posts) - 1]
    return {"details": post}


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db())):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    return {"Requested post": post}


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post, db: Session = Depends(get_db())):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    updated = post_query.first()
    
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    
    return {"data": updated}
    

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    
    post.delete(synchronize_session=False)
    db.commit()
    
    return {"deleted_post": post}