"""
This is the first program that will be executed when the server starts.
"""

from fastapi import FastAPI
from . import models
from . database import engine
from . routers import post, user, auth, vote

# Creates all the DB tables defined in models.py if not already present
models.Base.metadata.create_all(bind=engine)

# Creating our FastAPI instance
app = FastAPI()
        
# Separate routes to declutter the main file and improve readability
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)