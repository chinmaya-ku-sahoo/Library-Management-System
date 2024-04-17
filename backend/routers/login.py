from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from connect_db import get_db
from schemas import schema
from authentication.authenticate import authenticate_user

router = APIRouter(
    prefix="/v1"
)


@router.post("/login",
            tags=["Authentication"],
            status_code=200,
            summary="User Login",
            description="User Login")

async def user_login(response: Response, login_info: schema.LoginSchema, db: Session = Depends(get_db)):

    access_token = await authenticate_user(db, login_info, response)
    return {"message": "Login Successful!", 'AccessToken': access_token,  "statusCode": 200}
    