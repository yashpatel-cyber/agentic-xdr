from fastapi import APIRouter, Request

from app.core.config import settings
from app.schemas.response import APIResponse

router = APIRouter()


@router.get("/version", response_model=APIResponse)
async def version(request: Request):

    return APIResponse(
        message="Version information",
        data={
            "application": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.APP_ENV,
        },
        request_id=request.state.request_id,
    )