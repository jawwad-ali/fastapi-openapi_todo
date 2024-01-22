from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer 
 
from dbConnection import get_db, Session

from .utils import (
    ALGORITHM,
    JWT_SECRET_KEY
) 

# Types
from schema.types import SystemUser, TokenPayload, User

from jose import jwt
from pydantic import ValidationError

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)

def get_current_user(token: str = Depends(reuseable_oauth), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode( 
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        ) 
        token_data = TokenPayload(**payload) 
        print("Decoded Token Payload:", token_data)

        if datetime.fromtimestamp(token_data.exp) < datetime.now(): 
            raise HTTPException( 
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except (ValidationError): 
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.email == token_data.sub).first() 
    print("User from Database:", user)
    print("Token Data", token_data.sub) 

    if user is None:
        raise HTTPException( 
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return SystemUser(id=user.id, username=user.username, email=user.email)

db = Session()