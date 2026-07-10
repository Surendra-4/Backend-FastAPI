from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas, models
from .. database import get_db
from .. utils import verify_hash


router = APIRouter(
    tags=['Authentication']
)

@router.post('/login')
def user_login(auth: schemas.AuthBase, db: Session = Depends(get_db)):
    record = db.query(models.User).filter(models.User.email == auth.email).first()
    
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid credentials')
    
    if verify_hash(auth.password, record.password):
        return 'Login is successful'
    else:
        return 'Login is unsuccessful'