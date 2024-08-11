from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, Response, APIRouter
from .. import database, models, utils, schemas, oauth2

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db),
         current_user: int = Depends(oauth2.get_current_user)):
        
    # check to see if vote made by the same user already exists.
    # combining multiple filters.
    if not db.query(models.Post).filter(models.Post.id == vote.post_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Post with id: ({vote.post_id}) does not exist!")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if vote.dir == 1:
        
        if found_vote:
            # a conflicting voting relationship already exists in the db.
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user: ({current_user.id}) has already voted on post: ({vote.post_id})")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        
        return {"message":"successfully added vote"}

    else:
        # we cannot delete a post that does not exist.
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Vote does not exist")
        # delete the existing vote
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {'message':"successfull deleted vote"}
            
    



