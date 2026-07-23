from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(tags=["Version"])


@router.get("/version")
async def version():
    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
    }

@router.get("/crash")
async def crash():
    raise Exception("Test exception")