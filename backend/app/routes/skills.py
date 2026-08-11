from fastapi import APIRouter, HTTPException

from app.services.career_service import get_skills


router = APIRouter(
    prefix="/api/skills",
    tags=["Skills"]
)


@router.get("")
def skills():
    try:
        return get_skills()

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Unable to load skills"
        )