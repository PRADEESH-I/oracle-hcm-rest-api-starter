"""Fetch workers with their names embedded via the ``expand`` query parameter.

This is a small-but-important Oracle HCM REST pattern worth knowing early.

Child resources
---------------
In the Oracle Fusion REST model, a ``Worker`` is a parent resource that
has several child resources attached to it — ``names``, ``addresses``,
``emails``, ``assignments``, and so on. Each child is its own sub-
collection with its own URL, for example::

    /workers/{PersonId}/child/names

Without expansion, pulling a parent plus its children means an **N+1
query storm**: one ``GET /workers`` to list the people, then one
``GET /workers/{PersonId}/child/names`` per person to hydrate names.
Even 100 workers would cost 101 round-trips.

Why ``expand=names`` instead of separate calls
----------------------------------------------
The ``expand`` query parameter asks Oracle Fusion to inline a named
child resource directly inside each parent item in the same JSON
payload. One HTTP call, one TLS handshake, one auth round-trip. The
response for each worker then carries a ``names`` array of objects
(one per name type — Global, Legal, etc.), each with ``FirstName``,
``LastName``, ``Title``, and related fields.

How this demonstrates the HATEOAS pattern
-----------------------------------------
HATEOAS ("Hypermedia As The Engine Of Application State") is the REST
constraint that every response carries the links a client needs to
navigate to related resources — clients should not hand-craft URLs
from out-of-band knowledge. Every Oracle Fusion response includes a
``links`` array describing these transitions (``self``, ``canonical``,
``child``, ``parent``, ...). ``expand`` is the companion pattern: the
server *follows* those ``child`` links on behalf of the client and
inlines the result, so the client still honours the hypermedia
contract but avoids paying the round-trip cost.

Run:
    python examples/10_get_worker_names.py
"""

from hcm_client import Config, HCMClient


def main() -> None:
    client = HCMClient(Config.from_env(), verbose=True)
    data = client.get("/workers", params={"limit": 3, "expand": "names"})

    workers = data.get("items", [])
    print(f"\nFetched {len(workers)} worker(s) with expanded names:\n")

    for worker in workers:
        person_id = worker.get("PersonId")
        person_number = worker.get("PersonNumber")
        names = worker.get("names") or []

        print(f"  Worker PersonId={person_id} PersonNumber={person_number}")

        if not names:
            print("    (no names attached)")
            continue

        for name in names:
            name_type = name.get("NameType") or "-"
            title = name.get("Title") or "-"
            first = name.get("FirstName") or "-"
            last = name.get("LastName") or "-"
            print(f"    [{name_type}] Title={title} " f"FirstName={first} LastName={last}")


if __name__ == "__main__":
    main()
