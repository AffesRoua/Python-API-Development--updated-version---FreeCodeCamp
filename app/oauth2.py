import jwt 
from datetime import datetime,timedelta, timezone
from . import schemas 
from fastapi import status,Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import settings


#we already sent the client his access token to navigate 
#OAuth2PasswordBearer extract token when user use it to do thing related to him

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')# our path is "/login" so we just remove the "/""
#data is the payload 
#secret key is a parameter to have the signature withe the agorithm  ("function") ALGORITHM 
#ACCESS_TOKEN_EXPIRE_MINUTES is la durée de la session dés que user fait le login 
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire=datetime.now(timezone.utc)+timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_access_token(token:str,credentials_exception):
    try :
        payload =jwt.decode(token,settings.secret_key, algorithms=[settings.algorithm])

        id:str =payload.get("user_id")

        if id is None :
            raise credentials_exception
        else :
            tokendata=schemas.TokenData(id_tokendata=str(id))
    except jwt.PyJWTError:
            raise credentials_exception
    return tokendata

def get_current_user(token:str=Depends(oauth2_scheme)) :
    credentials_exception=HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,detail="could not validate credentials",
          headers={"WWW-Authenticate":"Bearer"})
    
    return verify_access_token(token,credentials_exception)