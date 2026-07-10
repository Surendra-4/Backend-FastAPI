from fastapi import FastAPI
from random import randrange
from pydantic import BaseModel
from typing import Optional
from fastapi import Response, status, HTTPException
import psycopg
from psycopg.rows import DictRow
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    
while True:
    try:
        conn = psycopg.connect(dbname="fastapi", user="postgres", password="56785678", host="localhost", row_factory=DictRow)
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
def create_post(post:Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 100000)
    my_posts.append(post_dict)
    return {"new_post": post_dict}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.get("/posts/latest")
def get_latest():
    post = my_posts[len(my_posts) - 1]
    return {"details": post}


@app.get("/posts/{id}")
def get_post(id: int):
    post = next((post for post in my_posts if post["id"] == id), None)
    return {"Requested post": post}


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, new_post: Post):
    
    index = None
    
    for i, post in enumerate(my_posts):
        if post['id'] == id:
            index = i
            break
    
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    
    my_posts[index] = new_post.model_dump()
    my_posts[index]['id'] = id
    
    return {"data": my_posts[index]}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = None
    
    for i, post in enumerate(my_posts):
        if post['id'] == id:
            index = i
            break
    
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id: {id} is not found")        

    my_posts.pop(index)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)