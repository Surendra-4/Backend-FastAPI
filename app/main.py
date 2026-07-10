from fastapi import FastAPI

import psycopg
from psycopg.rows import dict_row
import time

from . import models
from . database import engine
from . routers import post, user, auth

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
        
        
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)