from statistics import mode
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from app.model import Vote
from app import schema, database, model, Oauth2
from sqlalchemy.orm import Session

router=APIRouter(prefix="/vote", tags=['Vote'])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schema.Vote, db: Session=Depends(database.get_db), Current_user: int=Depends(Oauth2.get_current_user)):

    post=db.query(model.Post).filter(model.Post.id==vote.post_id).first()

    if not post:    
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {vote.post_id} doesnot exist")

    Vote_query=db.query(model.Vote).filter(model.Vote.post_id==vote.post_id, model.Vote.user_id==Current_user.id)
    found_vote=Vote_query.first()
    if (vote.dir==1): 
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{Current_user.id} has already voted on post {vote.post_id}")
        
        new_vote=model.Vote(post_id=vote.post_id, user_id=Current_user.id)
        db.add(new_vote)
        db.commit() 
        return {"message": "succesfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote doesnot exist")

        Vote_query.delete(synchronize_session=False)
        db.commit()
        return{"message": "successfully deleted Vote"}

        

