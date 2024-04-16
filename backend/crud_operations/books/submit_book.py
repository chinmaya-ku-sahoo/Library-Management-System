from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import update, select

from models import models

async def return_book_by_borrow_id(db: Session, user_id, borrow_id):
    user_borrow = db.query(models.BorrowingHistory).filter(models.BorrowingHistory.user_id == user_id,
                                            models.BorrowingHistory.borrow_id == borrow_id).first()
    if not user_borrow:
        raise HTTPException(status_code=404, detail={"message": f"Borrow Id {borrow_id} not found for logged-in user"})
    
    if user_borrow.returned:
        raise HTTPException(status_code=422, detail={"message": f"Book already returned"})

    try:
        db.query(models.BorrowingHistory)\
        .filter(models.BorrowingHistory.borrow_id == borrow_id, models.BorrowingHistory.user_id == user_id)\
        .update({models.BorrowingHistory.returned: True})

        # Create a subquery to join the tables and filter by borrow_id
        subquery = select(models.Book)\
            .join(models.BorrowingDetails, models.Book.book_id == models.BorrowingDetails.book_id)\
            .filter(models.BorrowingDetails.borrow_id == borrow_id).subquery()

        # Update the available_copies column using the subquery
        stmt = update(models.Book)\
            .where(models.Book.book_id == subquery.c.book_id)\
            .values(available_copies=models.Book.available_copies + 1)

        # Execute the update statement
        db.execute(stmt)        
        db.commit()
        
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail={"message": f"Unable to return the books due to {e}"})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail={"message": f"Unable to return the books due to {e}"})