from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from sqlalchemy.exc import SQLAlchemyError

from models import models

async def renew_book_by_borrow_id(db: Session, user_id, borrow_id):
    
    user_borrow = db.query(models.BorrowingHistory).filter(models.BorrowingHistory.user_id == user_id, models.BorrowingHistory.borrow_id == borrow_id).first()
    if not user_borrow:
        raise HTTPException(status_code=404, detail={"message": f"Borrowing id {borrow_id} not found for logged-in user"})

    try:
        
        old_return_date = user_borrow.return_date
        new_date = old_return_date+timedelta(days=30)

        db.query(models.BorrowingHistory)\
        .filter(models.BorrowingHistory.borrow_id == borrow_id, models.BorrowingHistory.user_id == user_id)\
        .update({models.BorrowingHistory.return_date: new_date, models.BorrowingHistory.reissued: True})
            
        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail={"message": f"Unable to renew books due to {e}"}) 
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=422, detail={"message": f"Unable to renew books due to {e}"})