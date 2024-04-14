from fastapi import HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from pathlib import Path
from sqlalchemy import func


from schemas import schema
from models.models import User
from .auth import Auth

import base64
import json
import logging


auth_handler = Auth()


async def authenticate_user(db: Session, auth_info: schema.LoginSchema, response: Response):
    '''
    Method to authenticate user and return the AccessToken.
    '''

    user_info = db.query(User).filter(User.username == auth_info.username).first()

    if not user_info:
        raise HTTPException(status_code=404, detail="User not found")
    
    generated_psswrd = auth_handler.encode_psswrd(auth_info.password, user_info.salt)

    if generated_psswrd != user_info.password:
        raise HTTPException(status_code=401, detail="Wrong username/password")
    
    access_token = auth_handler.encode_token(str(user_info.user_id))
    response.set_cookie(key="access_token",value=access_token,httponly=True)
    return access_token

    # timestamp = datetime.now(datetime.UTC)
    
    # maxAge = datetime.now() + timedelta(days=0, minutes=30)


    # input_username = user_details.username
    # username = input_username.lower()
    

    # # Generating psswrd with user input.

            
    # today = datetime.now()
        
    # # Checking the psswrd expiry date.
    # expiry_date = db.query(Usermaster.psswrd_exp_date).filter(Usermaster.username == username).first()
    
    # if today >= expiry_date.psswrd_exp_date:
    #     exceptions(419,"419-A",errormessages["errormessagecode"]["773"])      
        
    # access_token = auth_handler.encode_token(str(id_user))
    # response.set_cookie(key="access_token",value=access_token,httponly=True)
    # return access_token
            