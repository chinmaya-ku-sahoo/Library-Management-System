from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from connect_db import get_db
from schemas import schema

from models import models


router = APIRouter(
    prefix="/v1"
)

@router.post("/users")
async def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    if user.userrole not in ("student", "librarian", "anonymous"):
        raise HTTPException(status_code=422, detail="Role is not defined")
    try:
        db_user = models.User(username=user.username, userrole=user.userrole, password = user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        # return db_user

        # return crud.create_user(db=db, user=user)
        return {
            "statuCode": 201,
            "message": "User created sucessfully"
        }
    except Exception as e:
        HTTPException(status_code=422, detail={"message": f"Unable to create tables due to {e}"})

