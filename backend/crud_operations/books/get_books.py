from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.models import BorrowingDetails, BorrowingHistory, Book

async def get_student_history(db: Session, user_id):
    
    try:
        borrow_details = db.query(BorrowingHistory.borrow_id, BorrowingHistory.return_date, BorrowingDetails.book_id, Book.title)\
        .join(BorrowingDetails, BorrowingHistory.borrow_id == BorrowingDetails.borrow_id)\
        .join(Book, BorrowingDetails.book_id == Book.book_id)\
        .filter(BorrowingHistory.user_id == user_id).all()
        
        result = []
        for detail in borrow_details:
            result.append({
                "borrow_id": detail.borrow_id,
                "book_id": detail.book_id,
                "title": detail.title,
                "return_date": detail.return_date
            })

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail={"message": f"Unable fetch the history due to {e}"})


async def get_anonymous_history(db: Session):
    try:
        borrow_details = db.query(Book.title, Book.book_id, Book.available_copies).all()
        
        result = []
        for detail in borrow_details:
            result.append({
                "book_id": detail.book_id,
                "title": detail.title,
                "available_copies": detail.available_copies
            })

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail={"message": f"Unable fetch the history due to {e}"})


async def get_librarian_history(db: Session):
    try:
        result_list = []
        borrow_history = db.query(BorrowingHistory).all()
        if not borrow_history:
            return result_list
        for data in borrow_history:
            
            details_list = []
            
            borrow_details = db.query(BorrowingDetails.book_id, Book.title)\
            .join(Book, BorrowingDetails.book_id == Book.book_id)\
            .filter(BorrowingDetails.borrow_id == data.borrow_id).all()

            for detail in borrow_details:
                details_list.append({
                    "book_id": detail.book_id,
                    "title": detail.title
                })


            result_list.append(
                {
                    "user_id": data.user_id,
                    "borrow_date": data.borrow_date,
                    "return_date": data.return_date,
                    "reissued": data.reissued,
                    "returned": data.returned,
                    "history": details_list
                }
            )
        return result_list
    except Exception as e:
        raise HTTPException(status_code=500, detail={"message": f"Unable fetch the history due to {e}"})



