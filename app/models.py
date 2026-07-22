"""
This file contains sqlalchemy models of the tables we intend to keep in our database.
When the server starts, FastAPI checks for the presence of these tables.
If no table exists with the names defined in the models, new tables will be created.
If the table exists, it will be left untouched.
SQLAlchemy doesn't support Database migration (i.e., changing attributes, default values, data types).
Alembic supports migration.
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.sql import true
from sqlalchemy.orm import relationship
from .database import Base 

# This class defines the table 'posts'
class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default=true(), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('NOW()'), nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    owner = relationship('User')
    
    
# This class defines the table 'users'
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, nullable=False, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('NOW()'), nullable=False)