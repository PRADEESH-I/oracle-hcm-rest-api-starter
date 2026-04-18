# Getting started

This guide walks you from a fresh clone to your first successful call
against Oracle HCM Cloud.

## 1. Prerequisites

- Python 3.9 or later (`python --version`)
- `pip` (bundled with recent Python installers)
- Access to an Oracle HCM Cloud pod (any Oracle-provided Fusion
  Applications public demo pod works for read-only calls if you have
  credentials for it)

## 2. Clone the repo

```bash
git clone https://github.com/PRADEESH-I/oracle-hcm-rest-api-starter.git
cd oracle-hcm-rest-api-starter
```

## 3. Create a virtual environment

```bash
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Windows (Git Bash)
source .venv/Scripts/activate
```

## 4. Install the package

```bash
pip install -e .
```

For running tests as well:

```bash
pip install -e ".[dev]"
```

## 5. Configure your credentials

```bash
cp .env.example .env
```

Open `.env` and fill in:

| Variable          | Example                                                           |
| ----------------- | ----------------------------------------------------------------- |
| `HCM_BASE_URL`    | `https://your-fusion-pod.oraclecloud.com`                         |
| `HCM_API_VERSION` | `11.13.18.05`                                                     |
| `HCM_USERNAME`    | your HCM user (e.g. `FAAdmin`)                                    |
| `HCM_PASSWORD`    | your HCM password                                                 |

`.env` is git-ignored — it will never be committed.

## 6. Make your first call

```bash
python examples/01_get_workers.py
```

Expected output (truncated):

```
2026-04-18 10:15:03 [INFO] hcm_client.client: GET https://.../workers params={'limit': 3}
2026-04-18 10:15:04 [INFO] hcm_client.client: Response /workers: items=3 count=3 hasMore=True

Fetched 3 worker(s):
  - PersonId=300000001234567 PersonNumber=100001 DateOfBirth=1985-04-12
  ...
```

If you see errors, check [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

## 7. Try the other endpoints

```bash
python examples/02_get_jobs.py
python examples/03_get_departments.py
python examples/04_get_locations.py
python examples/05_get_grades.py
```

## 8. Next steps

- Read [ENDPOINTS.md](ENDPOINTS.md) for the full list of tested endpoints.
- Read [AUTHENTICATION.md](AUTHENTICATION.md) to understand how Basic Auth
  is wired up and what HCM roles you need.
- Run the test suite to see how the client behaves without hitting a real
  pod (see the README).
