from fastapi import APIRouter, Request

from app.core.config import settings
from app.schemas.response import APIResponse

router = APIRouter()


@router.get("/health", response_model=APIResponse)
async def health(request: Request):

    return APIResponse(
        message="Health check successful",
        data={
            "status": "healthy",
            "service": settings.APP_NAME,
            "version": settings.APP_VERSION,
        },
        request_id=request.state.request_id,
    )