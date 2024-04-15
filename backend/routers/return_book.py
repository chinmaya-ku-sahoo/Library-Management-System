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

@router.post("/return/{borrow_id}",
            tags=["Return Books"],
            status_code=201,
            description="Return Books Using Borrow Id")

async def return_book(borrow_id: str, db: Session = Depends(get_db),
                    credentials: HTTPAuthorizationCredentials = Security(security)):
    
    token = credentials.credentials
    user_id = auth_handler.decode_token(token)

    user_borrow = db.query(models.BorrowingHistory).filter(models.BorrowingHistory.user_id == user_id, models.BorrowingHistory.borrow_id == borrow_id).first()
    if not user_borrow:
        raise HTTPException(status_code=404, detail=f"Borrow Id {borrow_id} not found for logged-in user")
    
    if user_borrow.returned:
        raise HTTPException(status_code=422, detail=f"Book already returned")

    try:
        borrow_data = db.query(models.BorrowingHistory).filter(models.BorrowingHistory.borrow_id == borrow_id, models.BorrowingHistory.user_id == user_id).first()
        setattr(borrow_data, "returned", True)
        db.commit()
        db.refresh(borrow_data)
        
        return {
            "statuCode": 201,
            "message": "Book Returned Successfully"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=422, detail={"message": f"Unable to return books due to {e}"})
