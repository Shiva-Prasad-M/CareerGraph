from fastapi import APIRouter

from app.database.connection import database


router = APIRouter(
    prefix="/api",
    tags=["Health"]
)


@router.get("/health")
def health_check():
    database_status = database.verify_connection()

    if database_status:
        return {
            "status": "ok",
            "database": "connected"
        }

    return {
        "status": "error",
        "database": "unavailable"
    }