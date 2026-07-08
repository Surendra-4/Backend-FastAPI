from fastapi import FastAPI, Depends
from random import randrange
from pydantic import BaseModel
from typing import Optional
from fastapi import Response, status, HTTPException
import psycopg
from psycopg.rows import dict_row
import time
from app.database import get_db
from sqlalchemy.orm import Session
from app import models

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

@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    post.query.update(updated_post.model_dump())
    db.commit()