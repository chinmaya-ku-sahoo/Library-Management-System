from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from connect_db import get_db
from datetime import datetime, timedelta


from models import models


router = APIRouter(
    prefix="/v1"
)


@router.post("/students/{student_id}/borrow/{book_id}",
            tags=["Students"],
            status_code=201,
            description="Borrow Book")

async def borrow_book(student_id: int, book_id: int, db: Session = Depends(get_db)):

    user_role = db.query(models.User.userrole).filter(models.User.user_id == student_id).first()

    if not user_role:
        raise HTTPException(status_code=404, detail=f"User with id {student_id} not found")
    
    if user_role.userrole != "student":
        raise HTTPException(status_code=422, detail=f"User with id {student_id} is not a student")
    
    book_data = db.query(models.Book.book_id).filter(models.Book.book_id == book_id).first()
    if not book_data:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    
    
    try:

        today = datetime.now()
        return_date = today + timedelta(days=30)
        db_user = models.BorrowingHistory(user_id=student_id, book_id=book_id, borrow_date = today, return_date = return_date)
        db.add(db_user)
        
        # db.query(models.Book).filter(models.Book.book_id == book_id).update({models.Book.available_copies: models.Book.available_copies-1})
        book_data = db.query(models.Book).filter(models.Book.book_id == book_id).first()
        setattr(book_data, "available_copies", book_data.available_copies-1)
        
        db.commit()
        db.refresh(db_user)

        return {
            "statuCode": 201,
            "message": "User borrowed book successfully"
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=422, detail={"message": f"Unable to create tables due to {e}"})



@router.get("/students/{student_id}/books",
            tags=["Students"],
            status_code=200,
            description="Get student borrowing history")
async def get_student_history(student_id: int, db: Session = Depends(get_db)):

    user_role = db.query(models.User.userrole).filter(models.User.user_id == student_id).first()

    if not user_role:
        raise HTTPException(status_code=404, detail=f"User with id {student_id} not found")
    
    if user_role.userrole != "student":
        raise HTTPException(status_code=422, detail=f"User with id {student_id} is not a student")
    
    
    book_transactions = db.query(models.BorrowingHistory).filter(models.BorrowingHistory.user_id == student_id).all()
    if not book_transactions:
        raise HTTPException(status_code=422, detail=f"No borrowing history for thr user with id {student_id}")
    
    else:
        try:
        
            result = []
            for trans in book_transactions:
                book_details = db.query(models.Book.title).filter(models.Book.book_id == trans.book_id).first()
                result.append({
                        "title": book_details.title,
                        "borrow_date": trans.borrow_date,
                        "return_date": trans.return_date
                    }
                )

            return {
                        "statuCode": 200,
                        "message": "Record fetched successfully",
                        "detail": result
                    }

        except Exception as e:
            raise HTTPException(status_code=422, detail={"message": f"Unable to create tables due to {e}"})