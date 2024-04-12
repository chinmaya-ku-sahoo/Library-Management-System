from fastapi import HTTPException, APIRouter

from connect_db import Base, engine
from models import models


router = APIRouter(
    prefix="/v1"
)

@router.post("/create-table")
async def create_table():
    try:
        models.Base.metadata.create_all(bind=engine)
        return {
            "statuCode": 200,
            "message": "Successfully created the tables."
        }
    except Exception as e:
        HTTPException(status_code=422, detail={"message": f"Unable to create tables due to {e}"})

