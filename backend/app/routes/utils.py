from fastapi import APIRouter, HTTPException

from app.services.external_service import ping_external_service

router = APIRouter(prefix="/utils", tags=["Utilities"])


@router.get("/external-check")
async def external_check() -> dict:
    try:
        return await ping_external_service()
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"External service failed: {exc}") from exc
