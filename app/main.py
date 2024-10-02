from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post,user,auth,vote
from .config import settings 

from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins=["*"]# we allow every single domain to send requests to our api 
app.add_middleware(
    CORSMiddleware,#a function that runs before every request 
    allow_origins=origins,# what domains should we allow to send requests to our api 
    allow_credentials=True,
    allow_methods=["*"],# what methods to allow , get ?, put ? ...
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
@app.get("/")
def root():
    return {"message": "Hello Roua Affes"}

