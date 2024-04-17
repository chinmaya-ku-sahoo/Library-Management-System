from fastapi import APIRouter, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from connect_db import get_db
from schemas import schema
from authentication.auth import Auth

from crud_operations.books.add_books import add_books
from crud_operations.books.get_books import get_books


router = APIRouter(
    prefix="/v1"
)

security = HTTPBearer()
auth_handler = Auth()

@router.post("/books",
            status_code=201,
            tags=["Books"],
            summary="Register a Book",
            response_description="Book Registered Successfully")

async def store_books(book: schema.BookBase, db: Session = Depends(get_db),
                       credentials: HTTPAuthorizationCredentials = Security(security)):
    
    await add_books(db, book)
    return {
            "statusCode": 201,
            "message": "Book Registered Successfully"
        }


@router.get("/books",
            status_code=200,
            tags=["Books"],
            summary="Get All Books")

async def get_all_books(db: Session = Depends(get_db), 
                        credentials: HTTPAuthorizationCredentials = Security(security)):
    
    token = credentials.credentials
    user_id = auth_handler.decode_token(token)
    details = await get_books(db)
    return {
            "statuCode": 200,
            "message": "Books Fetched Sucessfully",
            "detail": details
        }
