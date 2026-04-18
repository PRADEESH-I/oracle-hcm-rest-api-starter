"""Tests for :class:`hcm_client.HCMClient` using the ``responses`` library.

All HTTP traffic is mocked, so these tests run without network access
and without real Oracle HCM credentials.
"""

import json
from pathlib import Path

import pytest
import responses

from hcm_client import Config, HCMClient
from hcm_client.errors import AuthError, HCMError, NotFoundError, ServerError

_FIXTURES = Path(__file__).parent / "fixtures"
_API_ROOT = "https://example.oraclecloud.com/hcmRestApi/resources/11.13.18.05"


def _load_fixture(name: str) -> dict:
    with open(_FIXTURES / name, encoding="utf-8") as fh:
        return json.load(fh)


@pytest.fixture
def config() -> Config:
    return Config(
        base_url="https://example.oraclecloud.com",
        api_version="11.13.18.05",
        username="test_user",
        password="test_pass",
        timeout=5.0,
        verify_ssl=True,
    )


@pytest.fixture
def client(config) -> HCMClient:
    return HCMClient(config, verbose=True)


@responses.activate
def test_get_workers_returns_parsed_json(client):
    payload = _load_fixture("workers_response.json")
    responses.add(
        responses.GET,
        f"{_API_ROOT}/workers",
        json=payload,
        status=200,
    )

    data = client.get("/workers", params={"limit": 3})

    assert "items" in data
    assert len(data["items"]) == 3
    assert data["items"][0]["PersonNumber"] == "100001"


@responses.activate
def test_get_jobs_uses_query_filter(client):
    payload = _load_fixture("jobs_response.json")
    responses.add(
        responses.GET,
        f"{_API_ROOT}/jobs",
        json=payload,
        status=200,
    )

    data = client.get("/jobs", params={"limit": 3, "q": "ActiveStatus=ACTIVE"})

    assert data["items"][0]["JobCode"] == "ENG_MGR"
    assert len(responses.calls) == 1
    assert "q=ActiveStatus%3DACTIVE" in responses.calls[0].request.url


@responses.activate
def test_401_raises_auth_error(client):
    responses.add(
        responses.GET,
        f"{_API_ROOT}/workers",
        json={"error": "unauthorized"},
        status=401,
    )

    with pytest.raises(AuthError):
        client.get("/workers")


@responses.activate
def test_403_raises_auth_error(client):
    responses.add(
        responses.GET,
        f"{_API_ROOT}/workers",
        json={"error": "forbidden"},
        status=403,
    )

    with pytest.raises(AuthError):
        client.get("/workers")


@responses.activate
def test_404_raises_not_found(client):
    responses.add(responses.GET, f"{_API_ROOT}/nope", status=404)

    with pytest.raises(NotFoundError):
        client.get("/nope")


@responses.activate
def test_400_raises_base_hcm_error(client):
    responses.add(
        responses.GET,
        f"{_API_ROOT}/workers",
        json={"error": "bad request"},
        status=400,
    )

    with pytest.raises(HCMError) as excinfo:
        client.get("/workers")

    assert not isinstance(excinfo.value, (AuthError, NotFoundError, ServerError))


@responses.activate
def test_500_retries_three_times_then_raises(client):
    url = f"{_API_ROOT}/workers"
    for _ in range(3):
        responses.add(responses.GET, url, status=500)

    with pytest.raises(ServerError):
        client.get("/workers")

    assert len(responses.calls) == 3


@responses.activate
def test_500_then_success_recovers(client):
    url = f"{_API_ROOT}/workers"
    responses.add(responses.GET, url, status=500)
    responses.add(responses.GET, url, json={"items": []}, status=200)

    data = client.get("/workers")

    assert data == {"items": []}
    assert len(responses.calls) == 2


@responses.activate
def test_post_sends_json_body(client):
    url = f"{_API_ROOT}/workers"
    responses.add(responses.POST, url, json={"PersonId": 1}, status=201)

    result = client.post("/workers", payload={"PersonNumber": "X1"})

    assert result == {"PersonId": 1}
    sent_body = json.loads(responses.calls[0].request.body)
    assert sent_body == {"PersonNumber": "X1"}
