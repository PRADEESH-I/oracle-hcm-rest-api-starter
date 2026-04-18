"""Fetch the first few workers from Oracle HCM Cloud.

Run:
    python examples/01_get_workers.py
"""

from hcm_client import Config, HCMClient


def main() -> None:
    client = HCMClient(Config.from_env(), verbose=True)
    data = client.get("/workers", params={"limit": 3})

    items = data.get("items", [])
    print(f"\nFetched {len(items)} worker(s):")
    for worker in items:
        print(
            f"  - PersonId={worker.get('PersonId')} "
            f"PersonNumber={worker.get('PersonNumber')} "
            f"DateOfBirth={worker.get('DateOfBirth')}"
        )


if __name__ == "__main__":
    main()
