from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from authentication.auth import Auth
from schemas import schema
from models import models

import os

def add_user(db: Session, user: schema.UserCreate):
    '''
    Function to add the user details to the users table.
    '''
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    try:
        salt = os.urandom(32)
        
        auth = Auth()
        hashed_psswrd = auth.encode_psswrd(user.password, salt)

        user_info = models.User(username=user.username, userrole=user.userrole, password = hashed_psswrd, salt = salt)
        db.add(user_info)
        db.commit()
        db.refresh(user_info)
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Unable to create user due to {e}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unable to create user due to {e}")