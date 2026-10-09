import json
import os
import pandas as pd
import boto3

from config import PROCESSED_DATA_DIR, RAW_DATA_DIR, STATES_STRING, PROCESSED_DATA_BUCKET_NAME

def upload_to_s3(file_path, bucket_name):
    file_name = os.path.basename(file_path)

    # AWS S3 upload setup
    session = boto3.Session(profile_name='Edsons-laptop')
    s3_client = session.client('s3')

    #upload files
    print(f"Uploading {file_name} to S3 bucket named {bucket_name}")
    s3_client.upload_file(file_path, bucket_name, file_name)



def load_raw(name: str) -> pd.DataFrame:
    path = os.path.join(RAW_DATA_DIR, f"{name}_{STATES_STRING}.json")

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

    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    csv_path = os.path.join(PROCESSED_DATA_DIR, f"bank_health_panel_{STATES_STRING}.csv")
    parquet_path = os.path.join(PROCESSED_DATA_DIR, f"bank_health_panel_{STATES_STRING}.parquet")
    panel.to_csv(csv_path, index=False)
    panel.to_parquet(parquet_path, index=False)

    #Upload the files to s3
    upload_to_s3(csv_path, PROCESSED_DATA_BUCKET_NAME)
    upload_to_s3(parquet_path, PROCESSED_DATA_BUCKET_NAME)



if __name__ == "__main__":
    #test transform in isolation
    main()