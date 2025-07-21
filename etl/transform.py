"""
transform.py

This module handles data transformation for multiple economic indicators (IPCA, SELIC, USD).
It cleans raw CSVs and outputs clean, standardized versions ready for analysis or loading.

Author: João Vítor Mendes
"""

import os
import pandas as pd

RAW_FOLDER = "../data"
CLEAN_FOLDER = "../data"
INDICATORS = ["ipca", "selic", "usd"]

def clean_bcb_data(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw data from the Central Bank of Brazil.

    Parameters:
        raw_df (pd.DataFrame): Raw DataFrame with 'date' and 'value' columns

    Returns:
        pd.DataFrame: Cleaned DataFrame with parsed dates and float values
    """
    print("[INFO] Cleaning data...")

    df = raw_df.copy()
    df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y", errors="coerce")
    df["value"] = df["value"].astype(str).str.replace(",", ".", regex=False)
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df.dropna(subset=["date", "value"], inplace=True)
    df.sort_values("date", inplace=True)

    print(f"[INFO] Cleaned {len(df)} valid rows.")
    return df

def process_indicator(indicator: str):
    """
    Processes and cleans a single indicator CSV file.

    Parameters:
        indicator (str): Name of the indicator (e.g., 'ipca')
    """
    raw_path = os.path.join(RAW_FOLDER, f"{indicator}_raw.csv")
    clean_path = os.path.join(CLEAN_FOLDER, f"{indicator}_clean.csv")

    print(f"\n[PROCESSING] {indicator.upper()}")

    if not os.path.exists(raw_path):
        print(f"[WARNING] File not found: {raw_path}")
        return

    raw_df = pd.read_csv(raw_path)
    cleaned_df = clean_bcb_data(raw_df)

    cleaned_df.to_csv(clean_path, index=False)
    print(f"[SUCCESS] Saved cleaned data to: {clean_path}")

if __name__ == "__main__":
    print("[START] Transformation Pipeline")

    for indicator in INDICATORS:
        process_indicator(indicator)

    print("\n[END] All transformations completed successfully.")