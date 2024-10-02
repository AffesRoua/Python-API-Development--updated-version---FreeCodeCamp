from fastapi import status,Depends,APIRouter,HTTPException
from sqlalchemy.orm import Session
from .. import oauth2,models,utils
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db


router=APIRouter(tags=['Authentication'])

@router.post("/login")
def login(user_credentials:OAuth2PasswordRequestForm=Depends(),db: Session = Depends(get_db)):

    #OAuth2PasswordRequestForm makes the credentials composed of two fields 
    #username(even though it contains the email for us ) and password because is of type UserLogin
    user=db.query(models.Users).filter(models.Users.email==user_credentials.username).first()

    if not user :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    elif not utils.verify_password(user_credentials.password,user.password) :#it is stored in databases hashed password
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    else :
        access_token=oauth2.create_access_token(data={"user_id":user.id})
    
    return{"access_token":access_token,"token_type":"bearer"}

