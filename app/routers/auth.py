from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app import schema, model, util, Oauth2

router=APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schema.Token)
def login(user_credintials: OAuth2PasswordRequestForm=Depends(), db: Session= Depends(get_db)):
    user=db.query(model.User).filter(model.User.email==user_credintials.username).first()
    

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invald credentials")
    
    if not util.verify(user_credintials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invald credentials")
    
    access_token=Oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

    



