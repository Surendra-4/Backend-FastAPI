from app.schemas import AuthBase
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException, status
from ..app import models
from fastapi.security import OAuth2PasswordRequestForm
from app.utils import verify_hash
from temp_oauth2 import create_access_token

router = APIRouter()

@router.post('/login')
def user_login(auth: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == auth.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid credentials')

    if verify_hash(auth.password, user.password):
        jwt = create_access_token({'email':auth.username})
        return {'access_token': jwt, 'token_type': 'bearer'}
    
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid credentials')