from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError


from schemas import schema
from models import models

async def borrow_books(db: Session, books: schema.BorrowingDetails, user_id):
    user_role = db.query(models.User.userrole).filter(models.User.user_id == user_id).first()

    if not user_role:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    
    if user_role.userrole != "student":
        raise HTTPException(status_code=422, detail=f"User with id {user_id} is not a student")
    
    book_id = books.book_ids
    if len(book_id) != len(set(book_id)):
        raise HTTPException(status_code=422, detail=f"Provide unique book ids")
    
    db_book = db.query(models.Book.book_id).all()
    if not db_book:
        raise HTTPException(status_code=404, detail=f"Book not found")
    
    db_book_list = [id[0] for id in db_book]
    if not all(id in db_book_list for id in book_id):
        raise HTTPException(status_code=404, detail=f"Invalid book id provided")    
    
    try:

        today = datetime.now()
        return_date = today + timedelta(days=30)
        db_user = models.BorrowingHistory(user_id=user_id, borrow_date = today, return_date = return_date)
        db.add(db_user)
        db.commit()

        borrowid = db_user.borrow_id

        # db.query(models.Book).filter(models.Book.book_id == book_id).update({models.Book.available_copies: models.Book.available_copies-1})
        for id in book_id:
            book_detail = models.BorrowingDetails(borrow_id = borrowid, book_id = id)
            db.add(book_detail)

            book_data = db.query(models.Book).filter(models.Book.book_id == id).first()
            setattr(book_data, "available_copies", book_data.available_copies-1)
        
        db.commit()
        db.refresh(db_user)

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail={"message": f"Unable to borrow books due to {e}"})
    
    except Exception as e:
        raise HTTPException(status_code=422, detail={"message": f"Unable to borrow books due to {e}"})