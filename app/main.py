"""
This is the first program that will be executed when the server starts.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . routers import post, user, auth, vote

# Creating our FastAPI instance
app = FastAPI()

origins = [
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
        
# Separate routes to declutter the main file and improve readability
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)