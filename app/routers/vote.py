from fastapi import APIRouter, Depends, HTTPException, status
from .. import models, schemas
from .. oauth2 import get_current_user
from sqlalchemy.orm import Session
from .. database import get_db

router = APIRouter(
    prefix='/vote', 
    tags = ['Vote']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def like(vote: schemas.Vote, db: Session = Depends(get_db),
        current_user: schemas.UserResponse = Depends(get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == vote.post_id)
    
    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id: {vote.post_id} does not exist')
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    
    if vote.direction:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = f'User already voted on the post')
        
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
        
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'Vote does not exist')
        
        db.delete(vote_query.first())
        db.commit()
        
        return {"message": "successfully deleted vote"}