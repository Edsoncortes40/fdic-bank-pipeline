"""
    Configurations for project!
"""

#FDIC API URL where data will be pulled from
API_BASE_URL = "https://api.fdic.gov/banks"

#The scope of this project only covers Banks in Maryland, for now
STATE = "MD"

#Only include institutions that are currently open. We don't need info on closed institutions.
ACTIVE_ONLY = True

#Scope of this project only calls for information that is dated back to 5 years at most
YEARS_OF_HISTORY = 5

#Page size placeholder for API calls. API DOC states default is 10, Maximum is 10,000
PAGE_SIZE = 100

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



