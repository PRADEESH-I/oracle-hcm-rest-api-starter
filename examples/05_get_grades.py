"""Fetch grades and show the common ``GradeCode`` / ``GradeName`` pattern.

Run:
    python examples/05_get_grades.py
"""

from hcm_client import Config, HCMClient


def main() -> None:
    client = HCMClient(Config.from_env(), verbose=True)
    data = client.get("/grades", params={"limit": 3})

    items = data.get("items", [])
    print(f"\nFetched {len(items)} grade(s):")
    for grade in items:
        print(
            f"  - {grade.get('GradeCode')}: {grade.get('GradeName')} "
            f"(ActiveStatus={grade.get('ActiveStatus')})"
        )


if __name__ == "__main__":
    main()
