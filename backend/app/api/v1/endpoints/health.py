from fastapi import APIRouter
from sqlalchemy import text

from app.database.session import engine

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health():

    db_status = "healthy"

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception:
        db_status = "unhealthy"

    return {
        "status": "healthy",
        "database": db_status,
    }