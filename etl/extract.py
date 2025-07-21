"""
extract.py

This module handles data extraction from the Central Bank of Brazil's public API (SGS).
It fetches historical economic indicators (e.g. IPCA, SELIC, USD) and stores them locally.

Author: João Vítor Mendes
"""

import os
import requests
import pandas as pd
from datetime import datetime

# Constants
BASE_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs"
API_RESPONSE_FORMAT = "json"

# Mapping of indicators and output paths
INDICATORS = {
    "ipca": 433,
    "selic": 1178,
    "usd": 1
}
RAW_OUTPUT_FOLDER = "../data"

def fetch_bcb_series(series_id: int, start_date="2015-01-01", end_date=None) -> pd.DataFrame:
    """
    Fetches data from the Central Bank of Brazil API for a given SGS series ID.

    Parameters:
        series_id (int): SGS series ID (e.g. 433 for IPCA)
        start_date (str): Initial date in YYYY-MM-DD format
        end_date (str): Final date in YYYY-MM-DD format

    Returns:
        pd.DataFrame: Raw data as DataFrame with 'date' and 'value' columns
    """
    if end_date is None:
        end_date = datetime.today().strftime("%Y-%m-%d")

    # Restrict to 10 years max for daily series (as per BACEN API)
    if series_id in [1178, 1]:  # SELIC and USD
        ten_years_ago = datetime.today().replace(year=datetime.today().year - 10)
        start_dt = max(datetime.strptime(start_date, "%Y-%m-%d"), ten_years_ago)
        start_date = start_dt.strftime("%Y-%m-%d")

    start_fmt = datetime.strptime(start_date, "%Y-%m-%d").strftime("%d/%m/%Y")
    end_fmt = datetime.strptime(end_date, "%Y-%m-%d").strftime("%d/%m/%Y")

    endpoint = f"{BASE_URL}.{series_id}/dados"
    params = {
        "formato": API_RESPONSE_FORMAT,
        "dataInicial": start_fmt,
        "dataFinal": end_fmt
    }

    print(f"[INFO] Fetching series ID {series_id} from {endpoint}")
    response = requests.get(endpoint, params=params)

    if response.status_code != 200:
        raise Exception(f"[ERROR] Failed to fetch data: {response.status_code} - {response.text}")

    data = response.json()
    print(f"[INFO] Received {len(data)} records for series {series_id}")

    df = pd.DataFrame(data)
    df.columns = ["date", "value"]
    return df

def save_dataframe_to_csv(dataframe: pd.DataFrame, file_path: str):
    """
    Saves a DataFrame to a CSV file.

    Parameters:
        dataframe (pd.DataFrame): The DataFrame to be saved
        file_path (str): Destination file path
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    dataframe.to_csv(file_path, index=False)
    print(f"[SUCCESS] Data saved to {file_path}")

if __name__ == "__main__":
    print("[START] Extraction Pipeline")

    for name, series_id in INDICATORS.items():
        print(f"\n[INFO] Processing '{name.upper()}' series...")
        df = fetch_bcb_series(series_id)
        output_path = os.path.join(RAW_OUTPUT_FOLDER, f"{name}_raw.csv")
        save_dataframe_to_csv(df, output_path)

    print("\n[END] All extractions completed successfully.")