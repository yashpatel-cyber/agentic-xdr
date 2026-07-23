from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ErrorDetail(BaseModel):
    code: str
    message: str


class APIResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str = "Success"

    data: Optional[T] = None

    error: Optional[ErrorDetail] = None

    request_id: Optional[str] = None

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )