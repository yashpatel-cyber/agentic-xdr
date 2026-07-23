from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)-8s | "
    "%(name)s | "
    "%(message)s"
)


def setup_logging() -> logging.Logger:
    """
    Configure enterprise logging for Agentic-XDR.
    """

    logger = logging.getLogger("agentic_xdr")

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(LOG_FORMAT)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Application log
    app_handler = RotatingFileHandler(
        LOG_DIR / "app.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    app_handler.setFormatter(formatter)

    # Error log
    error_handler = RotatingFileHandler(
        LOG_DIR / "error.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(app_handler)
    logger.addHandler(error_handler)

    logger.propagate = False

    return logger


logger = setup_logging()