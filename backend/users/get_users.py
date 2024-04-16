from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import models

async def get_users(db: Session):
    
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=404, detail="Users not found")

    try:
        result = []
        for user in users:
            result.append(
                {
                "user_id": user.user_id,
                "username": user.username,
                "userrole": user.userrole
            })
        
        return result
    
    except Exception as e:
        HTTPException(status_code=500, detail={"message": f"Unable to fetch users due to {e}"})