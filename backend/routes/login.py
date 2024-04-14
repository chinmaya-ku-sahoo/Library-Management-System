from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from connect_db import get_db
from schemas import schema
from authentication.authenticate import authenticate_user

router = APIRouter(
    prefix="/v1"
)


@router.post("/login",
            tags=["Authentication"],
            status_code=200,
            description="User Login")

async def user_login(response: Response, login_info: schema.LoginSchema, db: Session = Depends(get_db)):

    access_token = await authenticate_user(db, login_info, response)
    return {"message": "Login Successful!", 'AccessToken': access_token,  "statusCode": 200}
    # user_role = db.query(models.User.userrole).filter(models.User.user_id == user_id).first()

    # if not user_role:
    #     raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    
    # if user_role.userrole != "student":
    #     raise HTTPException(status_code=422, detail=f"User with id {user_id} is not a student")
    
    # book_data = db.query(models.Book.book_id).filter(models.Book.book_id == book_id).first()
    # if not book_data:
    #     raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    
    
    # try:

    #     today = datetime.now()
    #     return_date = today + timedelta(days=30)
    #     db_user = models.BorrowingHistory(user_id=user_id, book_id=book_id, borrow_date = today, return_date = return_date)
    #     db.add(db_user)
        
    #     # db.query(models.Book).filter(models.Book.book_id == book_id).update({models.Book.available_copies: models.Book.available_copies-1})
    #     book_data = db.query(models.Book).filter(models.Book.book_id == book_id).first()
    #     setattr(book_data, "available_copies", book_data.available_copies-1)
        
    #     db.commit()
    #     db.refresh(db_user)

    #     return {
    #         "statuCode": 201,
    #         "message": "User borrowed book successfully"
    #     }
    # except Exception as e:
    #     print(e)
    #     raise HTTPException(status_code=422, detail={"message": f"Unable to create tables due to {e}"})
