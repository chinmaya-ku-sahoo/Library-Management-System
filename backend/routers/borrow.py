from fastapi import APIRouter, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from schemas.schema import BorrowingDetails
from connect_db import get_db
from authentication.auth import Auth
from crud_operations.books.borrow_books import borrow_books


router = APIRouter(
    prefix="/v1"
)

security = HTTPBearer()
auth_handler = Auth()

@router.post("/library/borrow",
            tags=["Borrow Books"],
            status_code=201,
            summary=["Borrow Books"],
            description="Borrow Books Based on Book Id")

async def borrow_book(books: BorrowingDetails, db: Session = Depends(get_db),
                    credentials: HTTPAuthorizationCredentials = Security(security)):
    
    token = credentials.credentials
    user_id = auth_handler.decode_token(token)
    
    await borrow_books(db, books, user_id)
    
    return {
            "statuCode": 201,
            "message": "Successfully Borrowed the Books "
        }
