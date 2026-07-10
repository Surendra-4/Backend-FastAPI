"""
auth.py contains routes associated with authentication.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas, models, oauth2
from .. database import get_db
from .. utils import verify_hash


router = APIRouter(
    tags=['Authentication']
)

# Path Operation Functions of "Authentication"

# Route dedicated to logging in an user
@router.post('/login')
def user_login(auth: schemas.AuthBase, db: Session = Depends(get_db)):
    record = db.query(models.User).filter(models.User.email == auth.email).first()
    
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid credentials')
    
    if verify_hash(auth.password, record.password):
        jwt_token = oauth2.create_access_token(data={"email": auth.email})
        return {"access_token": jwt_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid credentials')