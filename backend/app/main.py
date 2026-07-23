from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.lifespan import lifespan
from app.core.logging import logger
from app.middleware.logging import RequestLoggingMiddleware

logger.info("Starting Agentic-XDR Backend")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

# Request Logging Middleware
app.add_middleware(RequestLoggingMiddleware)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handlers
register_exception_handlers(app)

# API Routes
app.include_router(
    api_router,
    prefix="/api/v1",
)

@app.get("/")
async def root():
    return {
        "application": settings.APP_NAME,
        "status": "running",
    }