"""
This file is responsible for handling the database.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg://postgres:56785678@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Creating an instance of sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# This function returns a database session when request arrives
def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()