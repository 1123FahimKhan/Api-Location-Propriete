from fastapi import APIRouter, HTTPException
from app.services import service_resetdb

router = APIRouter(prefix="/admin/reset", tags=["admin/reset"])

@router.put("/")
def update_db():
    try:
        return service_resetdb.resetdb()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))