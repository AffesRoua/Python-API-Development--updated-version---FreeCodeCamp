from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


#sqlalchemy doesn't put changes to tables after they are created , so at every change of a table the only solution
#is to drop the table and recreate it. This is a problem because it will delete all data

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
        orm_mode = True # this is to tell pydantic to convert the sqlalchemy object to dict 
                        #because by default only models can be converted to dict 

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