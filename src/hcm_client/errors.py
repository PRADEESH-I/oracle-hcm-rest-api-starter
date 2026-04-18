"""Custom exception hierarchy for the Oracle HCM REST client.

Keeping errors in their own module lets example scripts catch specific
failure modes (e.g. ``AuthError``) without importing the whole client.
"""


class HCMError(Exception):
    """Base class for every error raised by ``hcm_client``."""


class ConfigError(HCMError):
    """Raised when required configuration is missing or invalid."""


class AuthError(HCMError):
    """Raised on HTTP 401 (unauthenticated) or 403 (forbidden)."""


class NotFoundError(HCMError):
    """Raised on HTTP 404 — the endpoint or resource does not exist."""


class ServerError(HCMError):
    """Raised on HTTP 5xx responses (retried before being re-raised)."""


class TransientError(HCMError):
    """Raised on timeouts and connection errors (retried automatically)."""
