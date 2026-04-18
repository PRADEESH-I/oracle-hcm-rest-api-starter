"""Structured logging helpers for ``hcm_client``.

A single ``get_logger`` factory returns a module-scoped logger with a
consistent format across the client, examples, and tests.
"""

from __future__ import annotations

import logging
import sys

_LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_logger(name: str = "hcm_client", level: str = "INFO") -> logging.Logger:
    """Return a configured logger, creating handlers only once per name."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT))
        logger.addHandler(handler)
        logger.propagate = False
    logger.setLevel(level)
    return logger
