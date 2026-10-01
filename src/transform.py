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
    #left join on institutions and financials DataFrames on "CERT" column
    panel = financials.merge(institutions_meta, on="CERT", how="left")

    #convert REPDTE to date format that pandas can use, errors="coerce" will assign NaT in case conversion can't be made
    panel["REPDTE"] = pd.to_datetime(panel["REPDTE"], format="%Y%m%d", errors="coerce")
    #Sort by institution and REPDTE in Ascending order
    panel = panel.sort_values(by=["CERT", "REPDTE"], ascending=True)

    print(panel.head())




if __name__ == "__main__":
    #test transform in isolation
    main()