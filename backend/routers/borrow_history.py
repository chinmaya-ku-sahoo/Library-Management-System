from fastapi import APIRouter, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from connect_db import get_db
from models import models
from authentication.auth import Auth

from crud_operations.books import get_books_by_role


router = APIRouter(
    prefix="/v1"
)

security = HTTPBearer()
auth_handler = Auth()

@router.get("/library/books",
            status_code=200,
            tags=["Books"],
            summary="View Books Based on User Role")

async def get_books(db: Session = Depends(get_db), 
                        credentials: HTTPAuthorizationCredentials = Security(security)):
    
    token = credentials.credentials
    user_id = auth_handler.decode_token(token)

    user_role = db.query(models.User.userrole).filter(models.User.user_id == user_id).first()

    if user_role.userrole == "student":
        details = await get_books_by_role.get_student_history(db, user_id)
    
    elif user_role.userrole == "anonymous":
        details = await get_books_by_role.get_anonymous_history(db)

    else:
        details = await get_books_by_role.get_librarian_history(db)

    return {
            "statuCode": 200,
            "message": "Books fetched sucessfully",
            "detail": details
        }