"""
    For every institution in the raw institutions file, pull 5 years of
    quarterly financials (Call Report metrics) from the /financials endpoint
    and save the combined result.

    Requires ingest_institutions.py to have been run first.
"""

import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd

from fdic_client import fetch_all
from config import (
    FINANCIAL_FIELDS,
    STATES,
    RAW_DATA_DIR,
    YEARS_OF_HISTORY,
)


def load_certs(limit: int | None = None) -> list[str]:
    certs = []
    states_string = "_".join(STATES).lower()
    path = os.path.join(RAW_DATA_DIR, f"institutions_{states_string}.json")
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"File was not found! Run ingest_institutions.py first, make sure there is not limit on ingest_institutions.py"
        )

    with open(path) as f:
        payload = json.load(f)

    for rec in payload["records"]:
        if "CERT" in rec:
            certs.append(str(rec["CERT"]))

    #print(certs)
    return certs[:limit] if limit else certs


def date_filter() -> str:
    start_year = datetime.now(ZoneInfo("America/New_York")).year - YEARS_OF_HISTORY
    print(f"Starting year is {start_year}")

    return f"REPDTE:[{start_year}-01-01 TO *]"

def main(limit: int | None = None):
    certs = load_certs(limit)

    print(f"Pulling {YEARS_OF_HISTORY} years of financial for {len(certs)} Institutions!")

    all_records = []
    failed_records = []

    date_str = date_filter()
    #print(date_str)

    for i, cert in enumerate(certs, start=1):
        filters = f"CERT: {cert} AND {date_str}"
        print(filters)
        

        





if __name__ == "__main__":
    main()