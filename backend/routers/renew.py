from fastapi import APIRouter, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from connect_db import get_db
from authentication.auth import Auth
from crud_operations.books.renew_books import renew_book_by_borrow_id


router = APIRouter(
    prefix="/v1"
)

security = HTTPBearer()
auth_handler = Auth()

@router.put("/library/renew/{borrow_id}",
            tags=["Renew Books"],
            status_code=200,
            summary="Renew Book by Borrow Id",
            description="Renew Books Using Borrow Id")

async def renew_book(borrow_id: str, db: Session = Depends(get_db),
                    credentials: HTTPAuthorizationCredentials = Security(security)):
    
    token = credentials.credentials
    user_id = auth_handler.decode_token(token)

    await renew_book_by_borrow_id(db, user_id, borrow_id)
    return {
            "statuCode": 200,
            "message": "Book Renewed Successfully"
        }
