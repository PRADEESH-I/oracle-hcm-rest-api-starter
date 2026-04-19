# oracle-hcm-rest-api-starter

[![CI](https://github.com/PRADEESH-I/oracle-hcm-rest-api-starter/actions/workflows/ci.yml/badge.svg)](https://github.com/PRADEESH-I/oracle-hcm-rest-api-starter/actions/workflows/ci.yml)
[![Python versions](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> A beginner-friendly Python starter kit for calling the **Oracle HCM
> Cloud REST API**. Clone it, drop in your credentials, and have your
> first worker record back in under five minutes.

## Why this exists

New Oracle HCM consultants and developers almost always hit the same
wall on day one: **"I know the endpoint, I have credentials — now what
does a working client actually look like?"**

This repo answers that question with a production-shaped minimum:

- A small, reusable `hcm_client` package (auth, retries, timeouts,
  typed errors) — not a 30-line copy-paste snippet.
- One thin example script per tested endpoint.
- Mocked unit tests you can run without real credentials.
- Docs that cover setup, auth, endpoints, and troubleshooting.

All five example endpoints have been verified live against an Oracle
Fusion Applications public demo pod.

## Tested endpoints

| # | Resource    | Path                    | Example                          |
| - | ----------- | ----------------------- | -------------------------------- |
| 1 | Workers     | `/workers?limit=3`      | `examples/01_get_workers.py`     |
| 2 | Jobs        | `/jobs?limit=3`         | `examples/02_get_jobs.py`        |
| 3 | Departments | `/departments?limit=3`  | `examples/03_get_departments.py` |
| 4 | Locations   | `/locations?limit=3`    | `examples/04_get_locations.py`   |
| 5 | Grades      | `/grades?limit=3`       | `examples/05_get_grades.py`      |

Full field-level notes in [docs/ENDPOINTS.md](docs/ENDPOINTS.md).

### Advanced: expanding child resources

See [`examples/10_get_worker_names.py`](examples/10_get_worker_names.py)
for a short demo of the `expand` query parameter — it fetches each
worker's `names` child collection inline in a single round-trip,
avoiding the classic N+1 pattern of one request per child. The file's
docstring walks through the child-resource model, why `expand` beats
separate calls, and how the feature relates to the HATEOAS constraint.

## Quick start

```bash
# 1. Clone
git clone https://github.com/PRADEESH-I/oracle-hcm-rest-api-starter.git
cd oracle-hcm-rest-api-starter

# 2. Virtual env
python -m venv .venv
source .venv/bin/activate            # macOS / Linux
# .venv\Scripts\Activate.ps1         # Windows PowerShell

# 3. Install (editable)
pip install -e .

# 4. Configure
cp .env.example .env
# ... edit .env with your HCM_BASE_URL / HCM_USERNAME / HCM_PASSWORD ...

# 5. Run your first call
python examples/01_get_workers.py
```

Full walkthrough: [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md).

## Project structure

```
oracle-hcm-rest-api-starter/
├── README.md
├── LICENSE                       # MIT
├── .gitignore                    # Python + .env excluded
├── .env.example                  # copy to .env, never commit the real thing
├── pyproject.toml                # pip install -e . compatible
├── requirements.txt              # runtime dependencies
├── requirements-dev.txt          # adds pytest + responses
├── src/
│   └── hcm_client/               # reusable package
│       ├── __init__.py
│       ├── config.py             # loads .env, validates required vars
│       ├── client.py             # HCMClient (get/post, retries, timeouts)
│       ├── errors.py             # AuthError / NotFoundError / ServerError / ...
│       └── logging_utils.py      # structured logger
├── examples/                     # one thin script per endpoint
│   ├── 01_get_workers.py
│   ├── 02_get_jobs.py
│   ├── 03_get_departments.py
│   ├── 04_get_locations.py
│   └── 05_get_grades.py
├── tests/                        # pytest + responses (no live creds needed)
│   ├── test_client.py
│   ├── test_config.py
│   └── fixtures/
│       ├── workers_response.json
│       └── jobs_response.json
├── docs/
│   ├── GETTING_STARTED.md
│   ├── AUTHENTICATION.md
│   ├── ENDPOINTS.md
│   └── TROUBLESHOOTING.md
└── postman/
    └── README.md                 # Postman collection placeholder
```

## Using the client in your own code

```python
from hcm_client import Config, HCMClient

client = HCMClient(Config.from_env(), verbose=True)

workers = client.get("/workers", params={"limit": 5})
for w in workers["items"]:
    print(w["PersonNumber"], w.get("DateOfBirth"))
```

That's the whole API surface: `Config.from_env()` + `client.get()` /
`client.post()`. Errors raise typed exceptions from
`hcm_client.errors` (`AuthError`, `NotFoundError`, `ServerError`,
`TransientError`, `ConfigError`).

## How to run tests

Tests are fully offline — they mock HTTP traffic with the
[`responses`](https://github.com/getsentry/responses) library, so you
do **not** need real Oracle HCM credentials to run them.

```bash
# Install with dev extras
pip install -e ".[dev]"

# Run the suite
pytest
```

Expected output:

```
==================== test session starts ====================
tests/test_client.py ..........                        [ 71%]
tests/test_config.py .....                             [100%]
==================== 15 passed in ~5s ========================
```

The 5xx retry test intentionally takes a few seconds (exponential
backoff).

## Configuration reference

| Variable          | Required | Default       | Description                            |
| ----------------- | -------- | ------------- | -------------------------------------- |
| `HCM_BASE_URL`    | yes      | —             | Oracle Fusion pod URL, no trailing `/` |
| `HCM_USERNAME`    | yes      | —             | HCM user with REST privileges          |
| `HCM_PASSWORD`    | yes      | —             | User's password                        |
| `HCM_API_VERSION` | no       | `11.13.18.05` | REST resource version                  |
| `HCM_TIMEOUT`     | no       | `30`          | Per-request timeout, seconds           |
| `HCM_VERIFY_SSL`  | no       | `true`        | Set `false` only for local debugging   |

## Security

- `.env` is **never** committed — it is in `.gitignore`.
- Credentials are only held in-process (in a frozen `Config` dataclass
  and the `requests.Session` auth handler).
- TLS is on by default. If you need to turn it off for local
  debugging, use `HCM_VERIFY_SSL=false` and put it back immediately.

See [docs/AUTHENTICATION.md](docs/AUTHENTICATION.md) for deeper notes
on Basic Auth and when you should graduate to OAuth 2.0.

## Contributing

Issues and PRs are welcome — especially:

- Additional tested endpoints with sample scripts
- A real `.postman_collection.json` in `postman/`
- An OAuth 2.0 auth variant alongside Basic Auth

Please keep the starter beginner-friendly: every new example should
run end-to-end with just `.env` + `pip install -e .`.

## License

MIT — see [LICENSE](LICENSE).

## Acknowledgments

Built by [Pradeesh Irulappan](https://github.com/PRADEESH-I), Oracle HCM Consultant at Excelencia iTech Consulting, Chennai, India as part of the Oracle ACE Apprentice Program. Thanks to the Oracle Fusion Apps documentation team for the public demo environment that made live testing possible.
