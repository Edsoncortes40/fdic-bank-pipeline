"""
    Pull the roster of FDIC-insured institutions headquartered in the
    configured state and save it as raw JSON (source of truth) and a quick CSV
"""
import json
import os
#import pandas as pd
from fdic_client import fetch_all
from config import (
    ACTIVE_ONLY,
    STATE,
    INSTITUTION_FIELDS,
)

def build_filters() -> str:
    parts = [f"STALP:{STATE}"]
    if ACTIVE_ONLY:
        parts.append("ACTIVE:1")
    return " AND ".join(parts)

def main():
    filters = build_filters()
    print(filters)

if __name__ == "__main__":
    main()