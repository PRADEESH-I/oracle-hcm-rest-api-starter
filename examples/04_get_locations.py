"""Fetch physical locations and group them by country.

Run:
    python examples/04_get_locations.py
"""

from collections import defaultdict

from hcm_client import Config, HCMClient


def main() -> None:
    client = HCMClient(Config.from_env(), verbose=True)
    data = client.get("/locations", params={"limit": 3})

    items = data.get("items", [])
    by_country: dict[str, list[str]] = defaultdict(list)
    for loc in items:
        country = loc.get("Country") or "Unknown"
        name = loc.get("LocationName") or loc.get("LocationCode") or "(unnamed)"
        by_country[country].append(name)

    print(f"\nFetched {len(items)} location(s) across {len(by_country)} countr(y/ies):")
    for country, names in sorted(by_country.items()):
        print(f"  {country}: {', '.join(names)}")


if __name__ == "__main__":
    main()
