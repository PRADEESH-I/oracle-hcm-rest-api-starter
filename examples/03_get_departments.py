"""Fetch departments and show their linked location reference.

Run:
    python examples/03_get_departments.py
"""

from hcm_client import Config, HCMClient


def main() -> None:
    client = HCMClient(Config.from_env(), verbose=True)
    data = client.get("/departments", params={"limit": 3})

    items = data.get("items", [])
    print(f"\nFetched {len(items)} department(s):")
    for dept in items:
        print(
            f"  - {dept.get('Name')} "
            f"(DepartmentId={dept.get('DepartmentId')}, "
            f"LocationId={dept.get('LocationId')})"
        )


if __name__ == "__main__":
    main()
