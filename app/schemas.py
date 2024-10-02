from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint



class PostBase(BaseModel):#pydantic model
    title: str # mandatory
    content:str #mandatory 
    published: bool = True # here if the user doesn't specify the field it will be true by default 
    #rating: Optional[int]=None # this field peut être vide and not specified by the user 

class PostCreate(PostBase):
    pass


class UserCreate(BaseModel):
    email: EmailStr # mandatory
    password: str # mandatory


class UserResponse(BaseModel):
    email: EmailStr # mandatory
    id:int
    created_at:datetime
    class Config:
        orm_mode = True

class ResponsePost(BaseModel):#we are presicing the format of the response 
    title: str # mandatory
    content:str #mandatory 
    published: bool = True # here if the user doesn't specify the field it will be true by default 
    owner_id :int
    owner : UserResponse
    class Config:
        orm_mode = True 

class Post_vote(BaseModel):
    Post :ResponsePost #Post non post car par défaut c'est fait Post quand il générer 
    votes :int



class UserLogin(BaseModel):
    email: EmailStr # mandatory
    password:str
    class Config:
        orm_mode = True
class Token(BaseException):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id_tokendata: Optional[str] = None

class Vote(BaseModel):
    post_id:int 
    dir: int
