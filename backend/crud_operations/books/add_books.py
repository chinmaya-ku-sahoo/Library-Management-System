from fastapi import HTTPException
from sqlalchemy.orm import Session

from schemas import schema
from models import models


async def add_books(db: Session, book: schema.BookBase):

    # Check if book with the same title already exists
    existing_book = db.query(models.Book).filter(models.Book.title == book.title).first()
    if existing_book:
        raise HTTPException(status_code=400, detail="Book already exists")

    try:
        # Create new book record
        new_book = models.Book(title=book.title, total_copies=book.total_copies, available_copies=book.total_copies)
        db.add(new_book)
        db.commit()
        db.refresh(new_book)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Unable to store the book due to {e}")
