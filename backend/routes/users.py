from fastapi import HTTPException, APIRouter, Depends, Security
from sqlalchemy.orm import Session
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from connect_db import get_db
from schemas import schema
from models import models
from users.add_user import add_user
from authentication.auth import Auth


router = APIRouter(
    prefix="/v1"
)

security = HTTPBearer()
auth_handler = Auth()

@router.post("/users",
            tags=["Users"],
            description="Create a User",
            status_code=201)
async def create_user(user: schema.UserCreate, db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    user_id = auth_handler.decode_token(token)

    add_user(db, user)
    return {
        "statuCode": 201,
        "message": "User created successfully",
    }



@router.get("/users",
            tags=["Users"],
            description="Get All Users",
            status_code=200)
async def get_all_user(db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    user_id = auth_handler.decode_token(token)
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

