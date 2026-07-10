"""
This is the first program that will be executed after the server starts.
"""

from fastapi import FastAPI

import psycopg
from psycopg.rows import dict_row
import time

from . import models
from . database import engine
from . routers import post, user, auth

# Creates all the DB tables defined in models.py if not already present
models.Base.metadata.create_all(bind=engine)

# Creating our FastAPI instance
app = FastAPI()
    
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
        
        
# Separate routes to declutter the main file and improve readability
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)