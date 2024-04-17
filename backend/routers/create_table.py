from fastapi import HTTPException, APIRouter

from connect_db import Base, engine
from models import models


router = APIRouter(
    prefix="/v1"
)

@router.post("/create-table",
            tags=["Database"],
            status_code=201,
            summary="Create Table",
            description="Test Connection and Create Tables")
async def create_table():
    try:
        models.Base.metadata.create_all(bind=engine)
        return {
            "statuCode": 201,
            "message": "Successfully created the tables."
        }
    except Exception as e:
        HTTPException(status_code=422, detail={"message": f"Unable to create tables due to {e}"})

