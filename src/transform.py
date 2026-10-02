import json
import os
import pandas as pd

from config import PROCESSED_DATA_DIR, RAW_DATA_DIR, STATES

def load_raw(name: str) -> pd.DataFrame:
    states_string = "_".join(STATES).lower()
    path = os.path.join(RAW_DATA_DIR, f"{name}_{states_string}.json")

    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} not found! - Run the matching ingest script first!")
    
    #print(path)

    with open(path) as f:
        payload = json.load(f)

    return pd.DataFrame(payload["records"])


def main():
    institutions = load_raw("institutions")
    #print(institutions.head())

    financials = load_raw("financials")
    #print(financials.head())
    
    # Exlude data already included in financials data, since dropping columns, ensure no duplicates are present
    institutions_meta = institutions[["CERT", "NAME", "CITY", "STALP", "BKCLASS"]].drop_duplicates()
    # Left join on institutions and financials DataFrames on "CERT" column
    panel = financials.merge(institutions_meta, on="CERT", how="left")

    # Convert REPDTE to date format that pandas can use, errors="coerce" will assign NaT in case conversion can't be made
    panel["REPDTE"] = pd.to_datetime(panel["REPDTE"], format="%Y%m%d", errors="coerce")
    #Sort by institution and REPDTE in Ascending order
    panel = panel.sort_values(by=["CERT", "REPDTE"], ascending=True)

    # Groups rows by CERT (institution) and calculates the percentage change quarter-over-quarter for deposits in a new "dep_growth_qoq" column
    panel["dep_growth_qoq"] = panel.groupby("CERT")["DEP"].pct_change()

    # Groups rows by CERT (institution) and calculates the percentage change quarter-over-quarter for deposits in a new "dep_growth_qoq" column
    panel["asset_growth_qoq"] = panel.groupby("CERT")["ASSET"].pct_change()
    
    print(panel)




if __name__ == "__main__":
    #test transform in isolation
    main()