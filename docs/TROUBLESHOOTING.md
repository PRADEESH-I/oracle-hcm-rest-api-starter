# Troubleshooting

A quick index of the errors you are most likely to hit and how to fix
them.

## `AuthError: HTTP 401`

> `HTTP 401 from https://.../workers: {"error":"unauthorized"}`

- Double-check `HCM_USERNAME` and `HCM_PASSWORD` in `.env`.
- Try logging in to the HCM web UI with the same credentials.
- Passwords containing `#`, `$`, or `"` should not be quoted in `.env`
  unless the whole value is quoted. `python-dotenv` handles most cases,
  but if in doubt, put the value in single quotes.
- Account may be password-expired — reset it from the HCM UI.

## `AuthError: HTTP 403`

> `HTTP 403 from https://.../departments: ...`

The user is authenticated but does not have a role granting access to
this specific resource. Ask your HCM security admin to add an
aggregate privilege like `View Department` (or the equivalent custom
role) to the user.

## `NotFoundError: HTTP 404`

Either the path is wrong or the specific record does not exist.

- Confirm the API version in `HCM_API_VERSION` matches the pod.
- If you are hitting a by-id path like `/workers/{PersonId}`, confirm
  the id exists.

## `ServerError: HTTP 5xx` (after retries)

The client retries 3 times with exponential backoff. If all three fail:

- Check Oracle Cloud status for your region.
- The pod may be in maintenance — common for non-prod/demo pods.
- Try again in a few minutes.

## `TransientError: Network error ...`

- Check your internet connection.
- If you are on a corporate network, verify the pod host is not blocked
  by your firewall/proxy.
- Proxies: set `HTTPS_PROXY` and `HTTP_PROXY` environment variables;
  `requests` will pick them up automatically.

## `ssl.SSLCertVerificationError`

- Make sure your system trust store is up to date.
- As a last-resort debugging step, set `HCM_VERIFY_SSL=false` in
  `.env`. **Never** do this in production — you lose MITM protection.

## `ConfigError: Missing required environment variable(s): ...`

You haven't created `.env` yet, or it is missing required keys.

```bash
cp .env.example .env
# edit .env
```

## My script hangs forever

Oracle HCM calls can occasionally stall. The client uses `HCM_TIMEOUT`
(default 30 s) as a per-request timeout. Lower it if you prefer failing
fast:

```
HCM_TIMEOUT=10
```

## Imports fail: `ModuleNotFoundError: hcm_client`

Install the package in editable mode from the repo root:

```bash
pip install -e .
```

## Tests fail with "responses" not found

Install dev dependencies:

```bash
pip install -e ".[dev]"
```
