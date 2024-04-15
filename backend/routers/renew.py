from fastapi import HTTPException, APIRouter, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from sqlalchemy.orm import Session
from datetime import timedelta

from models import models
from connect_db import get_db
from authentication.auth import Auth


router = APIRouter(
    prefix="/v1"
)

security = HTTPBearer()
auth_handler = Auth()

@router.post("/renew/{borrow_id}",
            tags=["Renew Books"],
            status_code=201,
            description="Renew Books Using Borrow Id")

async def renew_book(borrow_id: str, db: Session = Depends(get_db),
                    credentials: HTTPAuthorizationCredentials = Security(security)):
    
    token = credentials.credentials
    user_id = auth_handler.decode_token(token)

    user_borrow = db.query(models.BorrowingHistory).filter(models.BorrowingHistory.user_id == user_id, models.BorrowingHistory.borrow_id == borrow_id).first()
    if not user_borrow:
        raise HTTPException(status_code=404, detail=f"Borrowing id {borrow_id} not found for logged-in user")
    

    try:
        borrow_data = db.query(models.BorrowingHistory).filter(models.BorrowingHistory.borrow_id == borrow_id).first()
        setattr(borrow_data, "reissued", True)
        
        old_return_date = borrow_data.return_date
        new_date = old_return_date+timedelta(days=30)
        setattr(borrow_data, "return_date", new_date)
            
        db.commit()
        db.refresh(borrow_data)
        
        return {
            "statuCode": 201,
            "message": "Book Renewed Successfully"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=422, detail={"message": f"Unable to renew books due to {e}"})
