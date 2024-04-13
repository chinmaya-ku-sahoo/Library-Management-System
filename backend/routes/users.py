from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from connect_db import get_db
from schemas import schema

from models import models


router = APIRouter(
    prefix="/v1"
)

@router.post("/users",
            tags=["Users"],
            description="Create a User",
            status_code=201)
async def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    try:
        db_user = models.User(username=user.username, userrole=user.userrole, password = user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return {
            "statuCode": 201,
            "message": "User created successfully"
        }
    except Exception as e:
        HTTPException(status_code=500, detail={"message": f"Unable to create user due to {e}"})


@router.get("/users",
            tags=["Users"],
            description="Get all Users",
            status_code=200)
async def get_all_user(db: Session = Depends(get_db)):

    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=404, detail="Users not found")

    try:
        result = []
        for user in users:
            result.append(
                {
                "user_id": user.user_id,
                "username": user.username,
                "userrole": user.userrole
            })

        return {
            "statuCode": 200,
            "message": "User details fetched successfully",
            "detail": result
        }
    except Exception as e:
        HTTPException(status_code=500, detail={"message": f"Unable to fetch users due to {e}"})

