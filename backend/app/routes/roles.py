from fastapi import APIRouter, HTTPException

from app.services.career_service import get_roles


router = APIRouter(
    prefix="/api/roles",
    tags=["Roles"]
)


@router.get("")
def roles():
    try:
        return get_roles()

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Unable to load roles"
        )