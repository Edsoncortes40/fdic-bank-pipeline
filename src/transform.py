import json
import os
import pandas as pd

from config import PROCESSED_DATA_DIR, RAW_DATA_DIR, STATES

def load_raw(name: str) -> pd.DataFrame:
    states_string = "_".join(STATES).lower()
    path = os.path.join(RAW_DATA_DIR, f"{name}_{states_string}.json")

    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} not found! - Run the matching ingest script first!")
    
    print(path)

    with open(path) as f:
        payload = json.load(f)

    return pd.DataFrame(payload["records"])


def main():
    institutions = load_raw("institutions")
    print(institutions.head())

    financials = load_raw("financials")
    print(financials.head())


if __name__ == "__main__":
    #test transform in isolation
    main()