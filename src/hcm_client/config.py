"""Configuration loader for the Oracle HCM REST client.

Values are pulled from environment variables, optionally bootstrapped by
a ``.env`` file via ``python-dotenv``. The resulting :class:`Config` is
frozen so it can be safely shared between threads.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

from .errors import ConfigError

_REQUIRED_VARS = ("HCM_BASE_URL", "HCM_USERNAME", "HCM_PASSWORD")
_DEFAULT_API_VERSION = "11.13.18.05"
_DEFAULT_TIMEOUT = "30"


@dataclass(frozen=True)
class Config:
    """Immutable connection settings for an Oracle HCM pod."""

    base_url: str
    api_version: str
    username: str
    password: str
    timeout: float = 30.0
    verify_ssl: bool = True

    @property
    def api_root(self) -> str:
        """Fully-qualified REST resource root, e.g. ``.../hcmRestApi/resources/11.13.18.05``."""
        return f"{self.base_url.rstrip('/')}/hcmRestApi/resources/{self.api_version}"

    @classmethod
    def from_env(cls, dotenv_path: Optional[str] = None) -> "Config":
        """Build a :class:`Config` from environment variables.

        A ``.env`` file in the repo root is loaded automatically; pass an
        explicit ``dotenv_path`` to override the lookup (useful in tests).

        Raises:
            ConfigError: if any required variable is missing.
        """
        load_dotenv(dotenv_path, override=False)

        missing = [name for name in _REQUIRED_VARS if not os.getenv(name)]
        if missing:
            raise ConfigError(
                "Missing required environment variable(s): "
                f"{', '.join(missing)}. Copy .env.example to .env and fill "
                "in your Oracle HCM credentials."
            )

        verify_raw = os.getenv("HCM_VERIFY_SSL", "true").strip().lower()
        return cls(
            base_url=os.environ["HCM_BASE_URL"].strip(),
            api_version=os.getenv("HCM_API_VERSION", _DEFAULT_API_VERSION).strip(),
            username=os.environ["HCM_USERNAME"],
            password=os.environ["HCM_PASSWORD"],
            timeout=float(os.getenv("HCM_TIMEOUT", _DEFAULT_TIMEOUT)),
            verify_ssl=verify_raw in ("1", "true", "yes", "on"),
        )
