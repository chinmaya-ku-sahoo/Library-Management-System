from fastapi import APIRouter, Depends, Security, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from connect_db import get_db
from schemas import schema
from models import models
from authentication.auth import Auth

from crud_operations.books.add_books import add_books
from crud_operations.books import get_books


router = APIRouter(
    prefix="/v1"
)

security = HTTPBearer()
auth_handler = Auth()

@router.post("/books",
            status_code=201,
            tags=["Books"],
            summary="Store a Book",
            response_description="Book Stored Successfully")

async def store_books(book: schema.BookBase, db: Session = Depends(get_db),
                       credentials: HTTPAuthorizationCredentials = Security(security)):
    
    await add_books(db, book)
    return {
            "statusCode": 201,
            "message": "Book stored successfully"
        }


@router.get("/books",
            status_code=200,
            tags=["Books"],
            summary="Fetch Books Based on Role")

async def get_all_books(db: Session = Depends(get_db), 
                        credentials: HTTPAuthorizationCredentials = Security(security)):
    
    token = credentials.credentials
    user_id = auth_handler.decode_token(token)

    user_role = db.query(models.User.userrole).filter(models.User.user_id == user_id).first()

    if user_role.userrole == "student":
        details = await get_books.get_student_history(db, user_id)
    
    elif user_role.userrole == "anonymous":
        details = await get_books.get_anonymous_history(db)

    else:
        details = await get_books.get_librarian_history(db)

    return {
            "statuCode": 200,
            "message": "Books fetched sucessfully",
            "detail": details
        }
