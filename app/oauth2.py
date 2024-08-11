# oauth2.py is for generating, verifying and dealing with all things token.

from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models, config
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

# this will help us extract the token from the...
# api request header.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    # we don't want to modify the data directly.
    # this is our payload
    to_encode = data.copy()
    # token expiration time
    # 30mins from now
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})

    # create the token
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str, credentials_exception):
    """verify the access token submitted by the user in each
    api request after logging in."""

    try: 
        print("here1")
        print(token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("here2")
        id: str = payload.get("user_id")

        if not id:
            raise credentials_exception
        
        # validate with our schema...
        # to see if the id is a string.
        token_data = schemas.TokenData(id=str(id))

    except JWTError:
        raise credentials_exception
    
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    """This will be passed as a dependency to our
    api request functions, it will validate the token
    submitted in the user's header and return the user's id
    or user account.
    
    This function allows us to return the user and all other
    neccessary logic eg profile, account, balance etc"""

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    
    # user's id
    user_id = verify_access_token(token, credentials_exception)

    # get user
    user = db.query(models.User).filter(models.User.id == user_id.id).first()
    
    return user