"""HTTP client for Oracle HCM Cloud REST endpoints.

The :class:`HCMClient` wraps :mod:`requests` with:

* HTTP Basic authentication sourced from :class:`~hcm_client.config.Config`
* Automatic retries on transient failures (timeouts, connection drops, 5xx)
  using exponential backoff via :mod:`tenacity`
* A single error-translation layer that maps HTTP status codes to the
  dedicated exceptions in :mod:`hcm_client.errors`
* An opt-in ``verbose`` mode that logs a compact summary of each response
"""
from __future__ import annotations

import json
import logging
from typing import Any, Dict, Optional

import requests
from requests.auth import HTTPBasicAuth
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from .config import Config
from .errors import (
    AuthError,
    HCMError,
    NotFoundError,
    ServerError,
    TransientError,
)
from .logging_utils import get_logger

logger = get_logger(__name__)


class HCMClient:
    """Thin, reusable client for Oracle HCM Cloud REST endpoints.

    Example:
        >>> from hcm_client import Config, HCMClient
        >>> client = HCMClient(Config.from_env(), verbose=True)
        >>> data = client.get("/workers", params={"limit": 3})
        >>> workers = data["items"]
    """

    def __init__(self, config: Config, verbose: bool = False) -> None:
        self.config = config
        self.verbose = verbose
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(config.username, config.password)
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

    def _url(self, endpoint: str) -> str:
        return f"{self.config.api_root}/{endpoint.lstrip('/')}"

    @retry(
        retry=retry_if_exception_type((TransientError, ServerError)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        before_sleep=before_sleep_log(logger, logging.INFO),
        reraise=True,
    )
    def get(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Issue a GET against an HCM REST endpoint and return parsed JSON."""
        url = self._url(endpoint)
        logger.info("GET %s params=%s", url, params or {})
        try:
            response = self.session.get(
                url,
                params=params,
                timeout=self.config.timeout,
                verify=self.config.verify_ssl,
            )
        except (requests.Timeout, requests.ConnectionError) as exc:
            raise TransientError(f"Network error calling {url}: {exc}") from exc

        self._raise_for_status(response)
        data = response.json()
        if self.verbose:
            self._log_summary(endpoint, data)
        return data

    @retry(
        retry=retry_if_exception_type((TransientError, ServerError)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        before_sleep=before_sleep_log(logger, logging.INFO),
        reraise=True,
    )
    def post(
        self,
        endpoint: str,
        payload: Dict[str, Any],
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Issue a POST with a JSON body and return parsed JSON."""
        url = self._url(endpoint)
        logger.info("POST %s", url)
        try:
            response = self.session.post(
                url,
                params=params,
                data=json.dumps(payload),
                timeout=self.config.timeout,
                verify=self.config.verify_ssl,
            )
        except (requests.Timeout, requests.ConnectionError) as exc:
            raise TransientError(f"Network error calling {url}: {exc}") from exc

        self._raise_for_status(response)
        return response.json()

    @staticmethod
    def _raise_for_status(response: requests.Response) -> None:
        if response.ok:
            return
        status = response.status_code
        body_preview = (response.text or "")[:500]
        message = f"HTTP {status} from {response.url}: {body_preview}"
        if status in (401, 403):
            raise AuthError(message)
        if status == 404:
            raise NotFoundError(message)
        if 500 <= status < 600:
            raise ServerError(message)
        raise HCMError(message)

    @staticmethod
    def _log_summary(endpoint: str, data: Dict[str, Any]) -> None:
        items = data.get("items")
        item_count = len(items) if isinstance(items, list) else "n/a"
        logger.info(
            "Response %s: items=%s count=%s hasMore=%s",
            endpoint,
            item_count,
            data.get("count"),
            data.get("hasMore"),
        )
