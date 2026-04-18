"""Oracle HCM Cloud REST API client — public package interface."""
from .client import HCMClient
from .config import Config
from .errors import (
    AuthError,
    ConfigError,
    HCMError,
    NotFoundError,
    ServerError,
    TransientError,
)

__version__ = "0.1.0"

__all__ = [
    "HCMClient",
    "Config",
    "HCMError",
    "ConfigError",
    "AuthError",
    "NotFoundError",
    "ServerError",
    "TransientError",
]
