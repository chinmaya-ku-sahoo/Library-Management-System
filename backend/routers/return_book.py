from fastapi import APIRouter, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from connect_db import get_db
from authentication.auth import Auth
from crud_operations.books.submit_book import return_book_by_borrow_id


router = APIRouter(
    prefix="/v1"
)

security = HTTPBearer()
auth_handler = Auth()

@router.post("/return/{borrow_id}",
            tags=["Return Books"],
            status_code=201,
            description="Return Books Using Borrow Id")

async def return_book(borrow_id: str, db: Session = Depends(get_db),
                    credentials: HTTPAuthorizationCredentials = Security(security)):
    
    token = credentials.credentials
    user_id = auth_handler.decode_token(token)

    await return_book_by_borrow_id(db, user_id, borrow_id)
    return {
            "statuCode": 201,
            "message": "Book Returned Successfully"
        }
