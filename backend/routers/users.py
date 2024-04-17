from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from connect_db import get_db
from schemas import schema
from users.add_user import add_user
from users.get_users import get_users
from authentication.auth import Auth


router = APIRouter(
    prefix="/v1"
)

security = HTTPBearer()

@router.post("/users",
            tags=["Users"],
            description="Create a User",
            summary="Create a User",
            status_code=201)
async def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):

    add_user(db, user)
    return {
        "statuCode": 201,
        "message": "User created successfully",
    }



@router.get("/users",
            tags=["Users"],
            description="Get All Users",
            summary="Get All Users",
            status_code=200)
async def get_all_user(db: Session = Depends(get_db), 
                       credentials: HTTPAuthorizationCredentials = Security(security)):
    
    token = credentials.credentials
    
    auth_handler = Auth()
    user_id = auth_handler.decode_token(token)

    result = await get_users(db)
    return {
        "statuCode": 200,
        "message": "User details fetched successfully",
        "detail": result
    }

