# Authentication

Oracle HCM Cloud REST APIs accept **HTTP Basic Authentication** out of
the box. This starter uses Basic Auth because it is the simplest path
from zero to a working call — which is the whole point of a starter.

## How it works in this repo

1. Credentials live in `.env` (git-ignored).
2. `Config.from_env()` reads `HCM_USERNAME` and `HCM_PASSWORD`.
3. `HCMClient.__init__` attaches an `HTTPBasicAuth(username, password)`
   handler to the underlying `requests.Session`, so every call carries
   an `Authorization: Basic <base64>` header.

No token cache, no OAuth dance, no refresh logic. Good enough for
learning, scripts, and internal tools.

## What kind of HCM user do I need?

The user in `.env` must:

- Exist in the target HCM pod as a **valid application user** (not just
  a worker).
- Have a job role that grants REST access to the resources you want to
  read — e.g. `Human Resource Specialist`, `Human Capital Management
  Integration Specialist`, or a custom role seeded with the right
  `*REST*` aggregate privileges.
- Not be locked out or password-expired.

For read-only exploration against a sandbox, a role with aggregate
privileges like `Manage Worker`, `View Job`, `View Department`,
`View Location`, and `View Grade` is enough.

## When Basic Auth is **not** enough

For production integrations, prefer one of:

- **OAuth 2.0** with a Fusion OAuth client (recommended by Oracle for
  machine-to-machine integrations).
- **JWT bearer tokens** issued by an IDCS / IAM Identity Domain.

This starter intentionally skips those — see Oracle's
[REST API for Oracle Fusion Cloud HCM](https://docs.oracle.com/en/cloud/saas/human-resources/farws/index.html)
for authoritative examples.

## Where the credentials go

| Layer              | Value used                                          |
| ------------------ | --------------------------------------------------- |
| `.env` file        | raw username + password (never committed)           |
| `Config` dataclass | `username`, `password` (immutable, in-process only) |
| `requests.Session` | `HTTPBasicAuth(username, password)` handler         |
| HTTP wire          | `Authorization: Basic base64(username:password)`    |

## Rotating credentials

Because credentials live only in `.env`, rotation is:

1. Update the password in HCM.
2. Edit `.env`.
3. Re-run any script.

No code change, no redeploy.
