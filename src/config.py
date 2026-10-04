"""
    Configurations for project!
"""

import os
from dotenv import load_dotenv
load_dotenv()


#FDIC API URL where data will be pulled from
API_BASE_URL = "https://api.fdic.gov/banks"

FDIC_API_KEY = os.getenv("FDIC_API_KEY")
if not FDIC_API_KEY:
    raise RuntimeError("FDIC_API_KEY is not set - make sure key is set in .env file!")


#The scope of this project covers the DMV area, including Maryland, Virginia and Washington DC.
STATES = ["MD", "VA", "DC"]
STATES_STRING = "_".join(STATES).lower()

#Only include institutions that are currently open. We don't need info on closed institutions.
ACTIVE_ONLY = True

#Scope of this project only calls for information that is dated back to 5 years at most
YEARS_OF_HISTORY = 5

#Page size placeholder for API calls. API DOC states default is 10, Maximum is 10,000
PAGE_SIZE = 100

# Path name for the raw data directory
RAW_DATA_DIR = "data/raw"

# Path name for the processed data directory
PROCESSED_DATA_DIR = "data/processed"

#Models for each API call. 
INSTITUTION_FIELDS = [
    "CERT",     # FDIC certificate number — primary key across all endpoints
    "NAME",     # Institution name
    "CITY",
    "STALP",    # State (2-letter)
    "ACTIVE",   # 1 = operating, 0 = closed/merged
    "BKCLASS",  # Charter class
    "ESTYMD",   # Date established
    "ASSET",    # Total assets ($ thousands), most recent quarter on file
    "DEP",      # Total deposits ($ thousands)
    "ROA",      # Return on assets
    "ROE",      # Return on equity
    "EQ",       # Total equity capital
]

FINANCIAL_FIELDS = [
    "CERT",     # FDIC certificate number — primary key across all endpoints
    "REPDTE",   # Report date (quarter end), e.g. 20260630
    "ASSET",
    "DEP",
    "NETINC",   # Net income
    "ROA",
    "ROE",
    "EQ",
    "LNLSNET",  # Net loans and leases
]



