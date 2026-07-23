from __future__ import annotations

import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log every incoming HTTP request.
    """

    async def dispatch(self, request: Request, call_next):

        request_id = str(uuid.uuid4())[:8]

        request.state.request_id = request_id

        start_time = time.perf_counter()

        response = await call_next(request)

        duration = (time.perf_counter() - start_time) * 1000

        client_ip = request.client.host if request.client else "unknown"

        logger.info(
            "[%s] %s %s %s -> %s (%.2f ms)",
            request_id,
            client_ip,
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )

        response.headers["X-Request-ID"] = request_id

        return response