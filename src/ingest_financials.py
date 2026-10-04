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

from fdic_client import fetch_all, FDICClientError
from config import (
    FINANCIAL_FIELDS,
    STATES_STRING,
    RAW_DATA_DIR,
    YEARS_OF_HISTORY,
)


def load_certs(limit: int | None = None) -> list[str]:
    certs = []
    path = os.path.join(RAW_DATA_DIR, f"institutions_{STATES_STRING}.json")
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
    #print(f"Starting year is {start_year}")

    return f"REPDTE:[{start_year}-01-01 TO *]"

def main(limit: int | None = None):
    certs = load_certs(limit)

    print(f"Pulling {YEARS_OF_HISTORY} years of financial for {len(certs)} Institutions!")

    all_records = []
    failed_certs = []

    date_str = date_filter()
    #print(date_str)

    for i, cert in enumerate(certs, start=1):
        filters = f"CERT: {cert} AND {date_str}"
        print(filters)
        try:
            records = fetch_all("financials", filters=filters, fields=FINANCIAL_FIELDS)
            all_records.extend(records)
            print(f"CERT #{i}: len(records) quarters pulled.")
        except FDICClientError as e:
            failed_certs.append(cert)
            print(f"CERT #{i}: CERT {cert} FAILED. - {e}")

    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    suffix = "_sample" if limit else ""
    raw_path = os.path.join(RAW_DATA_DIR, f"financials_{STATES_STRING}{suffix}.json")

    with open(raw_path, "w") as f:
        json.dump(
            {
                "fetched_at (EST)": datetime.now(ZoneInfo("America/New_York")).isoformat(sep=" "),
                "years_of_history:": YEARS_OF_HISTORY,
                "institution_count": len(certs),
                "failed_certs": failed_certs,
                "records": all_records,

            },
            f,
            indent=2,
        )

    print(f"saved json to {raw_path}")

    if all_records:
        df = pd.DataFrame(all_records)
        csv_path = os.path.join(RAW_DATA_DIR, f"financials_{STATES_STRING}{suffix}.csv")
        df.to_csv(csv_path, index=False)
        print(f"Saved csv to {csv_path}")
    if failed_certs:
        print(f"{len(failed_certs)} institutions failed to load: \n{failed_certs}")

    


if __name__ == "__main__":
    #Test by running python3 src/ingest_financials.py
    main()