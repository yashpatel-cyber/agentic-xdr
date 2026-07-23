from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.logging import logger


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Agentic-XDR API Started")

    yield

    logger.info("Agentic-XDR API Stopped")