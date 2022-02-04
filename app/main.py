
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
# import model                                              #before alembic 
# from database import engine
from app.routers import post, user, auth, vote
from app.config import Settings





# model.Base.metadata.create_all(bind=engine)       #before alembic 

app=FastAPI()

origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"Message": "this is the get method"}
 







