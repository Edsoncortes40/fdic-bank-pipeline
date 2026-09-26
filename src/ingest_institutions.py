"""
    Pull the roster of FDIC-insured institutions headquartered in the
    configured state and save it as raw JSON (source of truth) and a quick CSV
"""
import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd
from fdic_client import fetch_all
from config import (
    ACTIVE_ONLY,
    STATES,
    INSTITUTION_FIELDS,
    RAW_DATA_DIR
)

def build_filters() -> str:
    states_string = " OR ".join(STATES)
    parts = [f"STALP:({states_string})"]
    if ACTIVE_ONLY:
        parts.append("ACTIVE:1")
    return " AND ".join(parts)

def main(limit: int | None = None) -> None:
    filters = build_filters()
    print(f"Current filter string is: {filters}")
    if limit is not None:
        print(f"Current limit is: {limit}")

    records = fetch_all(
        endpoint="institutions",
        filters=filters,
        fields=INSTITUTION_FIELDS,
        max_records=limit,
    )

    if not records:
        print(f"fetch_all() did not return records inside ingest_institutions.py!")
        return

    #print(records)

    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    suffix = "_sample" if limit is not None else ""
    states_string = "_".join(STATES).lower()
    raw_path = os.path.join(RAW_DATA_DIR, f"institutions_{states_string}{suffix}") #why use os.join and not just a string concat?
    print(raw_path)

    with open(raw_path, "w") as f:
        json.dump(
            {
                "fetched_at (EST)" : datetime.now(ZoneInfo("America/New_York")).isoformat(), 
                "filters" : filters,
                "record_count": len(records),
                "records": records,
            },
            f, 
            indent=2,
        )
        print(f"saved json to {raw_path}")



if __name__ == "__main__":
    main(20)