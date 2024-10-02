from fastapi import Response,status,Depends,HTTPException,APIRouter
from .. import models,schemas,utils
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

router=APIRouter(
    prefix="/users/sqlalchemy",
    tags=['users'])

@router.post("/",response_model=schemas.UserResponse)

def create_posts_sqlalchemy(user:schemas.UserCreate,db: Session = Depends(get_db)):

    hashed_password=utils.hash_password(user.password)
    user.password=hashed_password

    new_user=models.Users(**user.model_dump())#it matches the fields automatically
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}",response_model=schemas.UserResponse )#the id here is a path parameter and is always retrieved as a string 
def get_user(id:int,response:Response,db: Session = Depends(get_db)):#id:int convert the id to number and give good message error if the id is not a number 
    #post=find_post(id) 
    #if id not found we want to have the 404 not found status code in postman and not 200ok so 
    user=db.query(models.Users).filter(models.Users.id==id).first()
    if not user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This user does not exist")
    else :
        return user