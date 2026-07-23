from __future__ import annotations

from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.logging import logger


def error_response(
    *,
    request_id: str,
    status_code: int,
    code: str,
    message: str,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error": {
                "code": code,
                "message": message,
            },
            "request_id": request_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )


def _http_error_response(
    request: Request,
    status_code: int,
    detail: str,
) -> JSONResponse:
    request_id = getattr(request.state, "request_id", "unknown")

    logger.warning(
        "[%s] HTTP %s - %s",
        request_id,
        status_code,
        detail,
    )

    return error_response(
        request_id=request_id,
        status_code=status_code,
        code="HTTP_ERROR",
        message=str(detail),
    )


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(HTTPException)
    async def fastapi_http_exception_handler(
        request: Request,
        exc: HTTPException,
    ):
        return _http_error_response(
            request,
            exc.status_code,
            str(exc.detail),
        )

    @app.exception_handler(StarletteHTTPException)
    async def starlette_http_exception_handler(
        request: Request,
        exc: StarletteHTTPException,
    ):
        return _http_error_response(
            request,
            exc.status_code,
            str(exc.detail),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ):
        request_id = getattr(request.state, "request_id", "unknown")

        logger.warning("[%s] Validation Error", request_id)

        return error_response(
            request_id=request_id,
            status_code=422,
            code="VALIDATION_ERROR",
            message="Request validation failed.",
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(
        request: Request,
        exc: Exception,
    ):
        request_id = getattr(request.state, "request_id", "unknown")

        logger.exception("[%s] Internal Server Error", request_id)

        return error_response(
            request_id=request_id,
            status_code=500,
            code="INTERNAL_SERVER_ERROR",
            message="An unexpected error occurred.",
        )