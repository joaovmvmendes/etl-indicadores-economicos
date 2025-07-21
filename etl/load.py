"""
load.py

This module loads cleaned economic indicators (IPCA, SELIC, USD) into a PostgreSQL database.

Author: João Vítor Mendes
"""

import os
import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL connection settings
DB_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "database": "economic_data",
    "user": "etl_user",
    "password": "123456"
}

CLEAN_FOLDER = "../data"
INDICATORS = ["ipca", "selic", "usd"]

def load_to_postgres(df: pd.DataFrame, table_name: str, db_config: dict):
    """
    Loads a DataFrame into a PostgreSQL table.

    Parameters:
        df (pd.DataFrame): The DataFrame to load
        table_name (str): Name of the target table
        db_config (dict): Connection settings
    """
    db_url = (
        f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}"
        f"@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    )

    print(f"[INFO] Connecting to PostgreSQL and loading table '{table_name}'...")
    engine = create_engine(db_url)
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"[SUCCESS] Loaded {len(df)} records into '{table_name}'.")

def process_indicator(indicator: str):
    """
    Loads a cleaned CSV into the database.

    Parameters:
        indicator (str): Name of the indicator (e.g., 'ipca')
    """
    csv_path = os.path.join(CLEAN_FOLDER, f"{indicator}_clean.csv")
    if not os.path.exists(csv_path):
        print(f"[WARNING] File not found: {csv_path}")
        return

    print(f"\n[PROCESSING] {indicator.upper()}")
    df = pd.read_csv(csv_path)
    load_to_postgres(df, indicator, DB_CONFIG)

if __name__ == "__main__":
    print("[START] PostgreSQL Load Pipeline")

    for indicator in INDICATORS:
        process_indicator(indicator)

    print("\n[END] All indicators loaded successfully.")