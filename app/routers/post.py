from statistics import mode
from app import schema, model, Oauth2
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from app.database import  get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

router=APIRouter(prefix="/posts", tags=['Posts'])

@router.get("/", response_model=List[schema.PostOut])
def get_post(db: Session = Depends(get_db), Current_user: int= Depends(Oauth2.get_current_user), limit: int=10, skip: int=0, search: Optional[str]=""):                        ##when using cursor.execute, no paramter to be passed in the function. Now, db parameter is getting parameter get_db from database.py file.
    # cursor.execute(""" SELECT * FROM posts""")
    # posts= cursor.fetchall()
   
    posts=db.query(model.Post, func.count(model.Vote.post_id).label("votes")).join(model.Vote, model.Vote.post_id==model.Post.id, 
    isouter=True).group_by(model.Post.id).filter(model.Post.title.contains(search)).limit(limit).offset(skip).all()   
    return posts




@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_posts(post: schema.PostCreate, db: Session = Depends(get_db), Current_user: int= Depends(Oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post=cursor.fetchone()
    # conn.commit()
    new_post=model.Post(owner_id=Current_user.id, **post.dict())                 ##unpacking a dict data type                    ##is similar to new_post=model.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post
 
@router.get("/{id}", response_model=schema.PostOut)
def get_post(id: int, db: Session = Depends(get_db), Current_user: int= Depends(Oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id= %s  """, (str(id)))
    # post=cursor.fetchone()

    post=db.query(model.Post, func.count(model.Vote.post_id).label("votes")).join(model.Vote, model.Vote.post_id==model.Post.id, 
    isouter=True).group_by(model.Post.id).filter(model.Post.id==id).first()   

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} was not found')

    return  post

#deleting a post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), Current_user: int= Depends(Oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id=%s RETURNING *""", (str(id),))
    # delpost=cursor.fetchone()
    # conn.commit()
    delpost=db.query(model.Post).filter(model.Post.id==id)
    if delpost.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} doesnot exist")
    if delpost.first().owner_id!= Current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    delpost.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

    


@router.put("/{id}")
def update_post(id: int, post: schema.PostCreate, db: Session = Depends(get_db), Current_user: int= Depends(Oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts  SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""",( post.title, post.content, post.published, str(id) ),)
    # updated_post=cursor.fetchone()
    # conn.commit()
    # index=find_index_post(id)
    updated_post=db.query(model.Post).filter(model.Post.id==id)
    if updated_post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post with id doesnot exist")
    if updated_post.first().owner_id!= Current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    updated_post.update({**post.dict()}, synchronize_session=False )
    db.commit()
    
    return updated_post.first()