from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base, engine

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Creating an instance of sessionmaker
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# This function returns a database session when request arrives
def get_test_db():
    db = TestSessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        
app.dependency_overrides[get_db] = get_test_db        

client = TestClient(app)