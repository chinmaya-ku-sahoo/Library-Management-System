from fastapi import HTTPException, Response
from sqlalchemy.orm import Session

from schemas import schema
from models.models import User
from .auth import Auth


auth_handler = Auth()


async def authenticate_user(db: Session, auth_info: schema.LoginSchema, response: Response):
    '''
    Method to authenticate user and return the AccessToken.
    '''

    user_info = db.query(User).filter(User.username == auth_info.username).first()

    if not user_info:
        raise HTTPException(status_code=404, detail={"message": "User not found"})
    
    generated_psswrd = auth_handler.encode_psswrd(auth_info.password, user_info.salt)

    if generated_psswrd != user_info.password:
        raise HTTPException(status_code=401, detail={"message": "Wrong username/password"})
    
    access_token = auth_handler.encode_token(str(user_info.user_id))
    response.set_cookie(key="access_token",value=access_token,httponly=True)
    return access_token
            