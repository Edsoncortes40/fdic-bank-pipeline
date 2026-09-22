"""
Python client that fetches data from the FDIC API

Docs: https://api.fdic.gov/banks/docs
Filter syntax is Elasticsearch query-string syntax, e.g.:
    STALP:MD
    STNAME:"Maryland" AND ACTIVE:1
    CERT:12345 AND REPDTE:[2020-01-01 TO *]
"""

from typing import Any

import requests

# Assumes API_BASE_URL and PAGE_SIZE live in your config.py per the
# outline — rename the import if you called them something else.
from config import API_BASE_URL, PAGE_SIZE


class FDICClientError(RuntimeError):
    """Raised when a request fails, or returns something that can't be parsed."""
    pass

def extract_records(payload: dict[str, Any]) -> list[dict[str, Any]]:
    if "data" in payload:
        data = payload["data"]
        if data and isinstance(data[0], dict) and "data" in data[0]:
            return [record["data"] for record in data]
        else:
            return []

def extract_total(payload: dict[str, Any]) -> int | None:
    if isinstance(payload, dict):
        metadata = payload.get("meta", {})
        total = metadata.get("total")
        if total is not None:
            return total
    else:
        print(f"payload is of type: {type(payload)}")


    print("total not found!")
    return None


def fetch_all(
    endpoint: str,
    filters: str | None = None,
    fields: list[str] | None = None,
    max_records: int | None = None,
    sort_by: str | None = None,
    page_size: int = PAGE_SIZE,
) -> list[dict[str, Any]]:
    """
    Page through an FDIC BankFind endpoint and return the full list of
    records (as plain dicts), stopping at max_records if given.

    endpoint: one of "institutions", "financials", "locations", "history",
              "failures", "sod", "summary", "demographics"
    """
    
    url = f"{API_BASE_URL}/{endpoint}"
    records: list[dict[str, Any]] = []
    offset = 0

    while True:
        limit = page_size
        if max_records is not None:
            limit = min(page_size, max_records - len(records))
            if limit <= 0:
                #All records processed, exit while loop
                break

            params = {"limit": limit, "offset": offset, "format": "json"}
            if filters:
                params["filters"] = filters
            if fields:
                params["fields"] = ",".join(fields)
            if sort_by:
                params["sort_by"] = sort_by

            resp = requests.get(url, params=params, timeout=30)
            #Raise error if response returns unsuccessful code
            if resp.status_code != 200:
                raise FDICClientError(
                    f"GET {resp.url} failed: STATUS CODE {resp.status_code}\n {resp.text}"
                )

            payload = resp.json()
            page = extract_records(payload)
            if not page:
                print("empty page returned!")
                break
            print(page)
            print("length of records: "  + str(len(page)))
            records.extend(page)
            offset += len(page)

            total = extract_total(payload)
            if total is not None:
                print(f"The meta total is: {total}")
            if total is None or offset >= total:
                break

    print(f"total records returned: {len(records)}")
    return records



if __name__ == "__main__":
    """
        Manual smoke test — run `python -m src.fdic_client` directly once fetch_all has a body. 
        Keep max_records tiny until you trust the shape.
    """
    #records = fetch_all("institutions", filters="STALP:MD", max_records=5)
    fetch_all(endpoint="institutions", filters="STALP:MD", max_records=10)
    #print(f"Got {len(records)} records")
    #for r in records:
    #    print(r)