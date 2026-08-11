from fastapi import APIRouter, HTTPException

from app.services.career_service import get_companies


router = APIRouter(
    prefix="/api/companies",
    tags=["Companies"]
)


@router.get("")
def companies():
    try:
        return get_companies()

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Unable to load companies"
        )