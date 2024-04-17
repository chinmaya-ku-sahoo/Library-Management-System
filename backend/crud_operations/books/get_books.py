from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import models

async def get_books(db: Session):
    books = db.query(models.Book).all()
    if not books:
        raise HTTPException(status_code=404, detail={"message": "Book not found"})

    try:
        result_list = []
        for book in books:
            result_list.append(
                {
                    "book_id": book.book_id,
                    "title": book.title,
                    "total_copies": book.total_copies,
                    "available_copies": book.available_copies
                }
            )

        return result_list
    
    except Exception as e:
        raise HTTPException(status_code=500, detail={"message": f"Unable to fetch the books due to {e}"})