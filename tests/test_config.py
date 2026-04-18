"""Tests for :class:`hcm_client.Config`.

These tests do not make any network calls — they only exercise the
environment-variable loading logic.
"""
import os

import pytest

from hcm_client import Config
from hcm_client.errors import ConfigError

_NO_DOTENV = os.path.join(os.path.dirname(__file__), "does_not_exist.env")


@pytest.fixture(autouse=True)
def _clear_env(monkeypatch):
    """Strip any HCM_* vars that might leak in from the developer's shell."""
    for key in (
        "HCM_BASE_URL",
        "HCM_API_VERSION",
        "HCM_USERNAME",
        "HCM_PASSWORD",
        "HCM_TIMEOUT",
        "HCM_VERIFY_SSL",
    ):
        monkeypatch.delenv(key, raising=False)


def test_from_env_success(monkeypatch):
    monkeypatch.setenv("HCM_BASE_URL", "https://example.oraclecloud.com")
    monkeypatch.setenv("HCM_USERNAME", "user")
    monkeypatch.setenv("HCM_PASSWORD", "secret")

    cfg = Config.from_env(dotenv_path=_NO_DOTENV)

    assert cfg.base_url == "https://example.oraclecloud.com"
    assert cfg.username == "user"
    assert cfg.password == "secret"
    assert cfg.api_version == "11.13.18.05"
    assert cfg.timeout == 30.0
    assert cfg.verify_ssl is True


def test_from_env_missing_required_raises(monkeypatch):
    monkeypatch.setenv("HCM_BASE_URL", "https://example.oraclecloud.com")

    with pytest.raises(ConfigError) as excinfo:
        Config.from_env(dotenv_path=_NO_DOTENV)

    message = str(excinfo.value)
    assert "HCM_USERNAME" in message
    assert "HCM_PASSWORD" in message


def test_api_root_strips_trailing_slash(monkeypatch):
    monkeypatch.setenv("HCM_BASE_URL", "https://example.oraclecloud.com/")
    monkeypatch.setenv("HCM_USERNAME", "u")
    monkeypatch.setenv("HCM_PASSWORD", "p")

    cfg = Config.from_env(dotenv_path=_NO_DOTENV)

    assert cfg.api_root == (
        "https://example.oraclecloud.com/hcmRestApi/resources/11.13.18.05"
    )


def test_verify_ssl_false_parsed(monkeypatch):
    monkeypatch.setenv("HCM_BASE_URL", "https://example.oraclecloud.com")
    monkeypatch.setenv("HCM_USERNAME", "u")
    monkeypatch.setenv("HCM_PASSWORD", "p")
    monkeypatch.setenv("HCM_VERIFY_SSL", "false")

    cfg = Config.from_env(dotenv_path=_NO_DOTENV)

    assert cfg.verify_ssl is False


def test_custom_timeout_and_version(monkeypatch):
    monkeypatch.setenv("HCM_BASE_URL", "https://example.oraclecloud.com")
    monkeypatch.setenv("HCM_USERNAME", "u")
    monkeypatch.setenv("HCM_PASSWORD", "p")
    monkeypatch.setenv("HCM_TIMEOUT", "45")
    monkeypatch.setenv("HCM_API_VERSION", "11.13.19.99")

    cfg = Config.from_env(dotenv_path=_NO_DOTENV)

    assert cfg.timeout == 45.0
    assert cfg.api_version == "11.13.19.99"
