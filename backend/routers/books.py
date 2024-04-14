from fastapi import HTTPException, APIRouter, Depends, Security, Response
from sqlalchemy.orm import Session
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from connect_db import get_db
from schemas import schema
from models import models
from authentication.auth import Auth


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
async def store_books(book: schema.BookBase, db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    user_id = auth_handler.decode_token(token)

    book_title = db.query(models.Book).filter(models.Book.title == book.title).first()
    if book_title:
        raise HTTPException(status_code=400, detail="Book already exist")

    try:
        book_data = models.Book(title=book.title, total_copies=book.total_copies, available_copies = book.total_copies)
        db.add(book_data)
        db.commit()
        db.refresh(book_data)

        return {
            "statuCode": 201,
            "message": "Book stored sucessfully"
        }
    
    except Exception as e:
        HTTPException(status_code=500, detail={"message": f"Unable to store book due to {e}"})


@router.get("/books",
            status_code=200,
            tags=["Books"],
            summary="Fetch all Books")
async def get_all_books(db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    user_id = auth_handler.decode_token(token)
    
    books = db.query(models.Book).all()
    if not books:
        raise HTTPException(status_code=404, detail="Books not found")

    try:
        all_book = []
        for book in books:
            all_book.append(
                {
                "book_id": book.book_id,
                "title": book.title,
                "total_copies": book.total_copies,
                "available_copies": book.available_copies
            })

        return {
            "statuCode": 200,
            "message": "Books fetched sucessfully",
            "detail": all_book
        }


    except Exception as e:
        HTTPException(status_code=500, detail={"message": f"Unable fetch books due to {e}"})
