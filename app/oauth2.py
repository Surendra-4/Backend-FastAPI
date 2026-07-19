import jwt
from jwt import PyJWTError
from datetime import datetime, timedelta, timezone
from fastapi import Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer 
from sqlalchemy.orm import Session

from . import schemas, models
from . database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET = '26ee0962f82f5bcf62da6be588a751df7656725c083fa8a50c390f6392f2a2d7'
ALGORITHM = 'HS256'
EXPIRATION_TIME = 60

def create_access_token(data: dict):
    """
    This function is responsible for creating JWT access tokens, which is then sent to the client.
    """
    
    to_encode = data.copy()
    to_encode['exp'] = datetime.now(timezone.utc) + timedelta(minutes=EXPIRATION_TIME)
    # to_encode.update({'exp': datetime.now() + timedelta(minutes=EXPIRATION_TIME)})
    
    jwt_token = jwt.encode(payload=to_encode, key=SECRET, algorithm=ALGORITHM)
    
    return jwt_token

def verify_access_token(token: str, credentials_exception):
    
    """
    This function is responsible for verifying if the access token is valid.
    It is called indirectly through get_current_user.
    If no errors, we return token data. (Meaning authentication is successful)
    """
        
    try:
        payload = jwt.decode(token, key=SECRET, algorithms=[ALGORITHM])

        # Sample output of payload: {'user_id': 12345, 'role': 'admin', 'exp': 1718900000}

        email: str = payload.get("email")

        if email is None:
            raise credentials_exception

        token_data = schemas.TokenData(email = email)
        
    except PyJWTError:
        raise credentials_exception
    
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    This function checks if the user is logged in.
    We pass this as a dependency in path operation functions that require user to be logged in.
    """    
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f'Invalid credentials', headers={'WWW-Authenticate': 'Bearer'})
    
    token_data = verify_access_token(token, credentials_exception)
    
    current_user = db.query(models.User).filter(models.User.email == token_data.email).first()
    
    return current_user


""" 
    # The following function can be used to fetch token data, it doesn't return user data
    
    def get_current_user(token: str = Depends(oauth2_scheme)):

    
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f'Invalid credentials', headers={'WWW-Authenticate': 'Bearer'})
    
    return verify_access_token(token, credentials_exception)
    
"""