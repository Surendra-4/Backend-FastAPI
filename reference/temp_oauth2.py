import jwt
from jwt import PyJWTError
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from app.database import get_db
from fastapi.security import OAuth2PasswordBearer
from ..app import models, schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET = '7eecd5c74e0efe40bcbab0003d1300ff79f8e2c90f849d1548e16626b0d79d7a'
ALGORITHM = 'HS256'
EXPIRATION_TIME = 5

def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode['exp'] = datetime.now(timezone.utc) + timedelta(minutes=EXPIRATION_TIME)
    token = jwt.encode(data, algorithm=ALGORITHM, key=SECRET)
    return token
    
    
def verify_access_token(token: str, credentials_exceptions):
    try:
        payload = jwt.decode(token, key=SECRET, algorithms=[ALGORITHM])
        
        email: str = payload.get('email')
        
        if email is None:
            raise credentials_exceptions
        
        token_data = schemas.TokenData(email=email)
        
    except PyJWTError:
        raise credentials_exceptions
    
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db : Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid Credentials',
                                        headers={'WWW-Authenticate': 'Bearer'})
    token_data = verify_access_token(token, credentials_exception)
    
    current_user = db.query(models.User).filter(models.User.email == token_data.username).first()
    
    return current_user