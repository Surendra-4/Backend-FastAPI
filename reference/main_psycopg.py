from fastapi import FastAPI
from random import randrange
from pydantic import BaseModel
from typing import Optional
from fastapi import Response, status, HTTPException
import psycopg
from psycopg.rows import dict_row
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool
    
    
# This loop ensures that we establish a DB connection before any request appears to the server   
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
def create_post(post: Post):
    cursor.execute(f"""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
                (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit() 
    return {"new_post": new_post}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.get("/posts/latest")
def get_latest():
    post = my_posts[len(my_posts) - 1]
    return {"details": post}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id=%s""", (str(id),))
    post = cursor.fetchone()
    return {"Requested post": post}


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    
    cursor.execute("""UPDATE posts SET title = %s, content=%s, published=%s WHERE id = %s RETURNING *""",
                (post.title, post.content, post.published, str(id)))
    updated = cursor.fetchone()
    
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    
    conn.commit()
    
    return {"data": updated}
    

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    post = cursor.fetchone()     
    conn.commit()
    return {"deleted_post": post}
