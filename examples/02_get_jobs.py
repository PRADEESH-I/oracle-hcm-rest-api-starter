"""Fetch active jobs from Oracle HCM Cloud.

Demonstrates server-side filtering via the ``q`` query parameter.

Run:
    python examples/02_get_jobs.py
"""
from hcm_client import Config, HCMClient


def main() -> None:
    client = HCMClient(Config.from_env(), verbose=True)
    data = client.get(
        "/jobs",
        params={"limit": 3, "q": "ActiveStatus=ACTIVE"},
    )

    items = data.get("items", [])
    print(f"\nFetched {len(items)} active job(s):")
    for job in items:
        print(
            f"  - {job.get('JobCode')}: {job.get('Name')} "
            f"(FullPartTime={job.get('FullPartTime')})"
        )


if __name__ == "__main__":
    main()
