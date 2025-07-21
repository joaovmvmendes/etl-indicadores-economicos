"""
app.py

Streamlit dashboard for visualizing economic indicators from PostgreSQL.

Author: João Vítor Mendes
"""

import io
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

# PostgreSQL connection settings
DB_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "database": "economic_data",
    "user": "etl_user",
    "password": "123456"
}

# Available economic indicators from SGS API
INDICATOR_MAP = {
    "IPCA": "ipca",
    "SELIC": "selic",
    "USD": "usd"
}

# Load data from PostgreSQL
@st.cache_data
def load_data(table_name):
    db_url = (
        f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )
    engine = create_engine(db_url)
    query = f"SELECT * FROM {table_name} ORDER BY date"
    df = pd.read_sql(query, engine)
    df["date"] = pd.to_datetime(df["date"])
    return df

# Streamlit UI
st.set_page_config(page_title="Economic Dashboard", layout="wide")
st.title("📊 Economic Indicator Dashboard")

# Sidebar: select indicator
st.sidebar.header("Configuration")
selected_indicator = st.sidebar.selectbox("Select Indicator", list(INDICATOR_MAP.keys()))
table_name = INDICATOR_MAP[selected_indicator]

# Load data
df = load_data(table_name)

# Sidebar: date range filter
df["date"] = pd.to_datetime(df["date"])
date_list = df["date"].dt.date
min_date = min(date_list)
max_date = max(date_list)

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Validate and apply filter
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    st.error("Please select a valid date range.")
    st.stop()

filtered_df = df[(df["date"] >= pd.to_datetime(start_date)) & (df["date"] <= pd.to_datetime(end_date))]

# KPIs summary
latest_value = filtered_df["value"].iloc[-1]
max_value = filtered_df["value"].max()
min_value = filtered_df["value"].min()

col1, col2, col3 = st.columns(3)
col1.metric(f"Latest {selected_indicator}", f"{latest_value:.2f}")
col2.metric("Max", f"{max_value:.2f}")
col3.metric("Min", f"{min_value:.2f}")

st.markdown(f"This dashboard displays historical data for **{selected_indicator}**, sourced from the Central Bank of Brazil.")

# Plot 1: line chart
st.subheader(f"{selected_indicator} Over Time")
st.line_chart(filtered_df.set_index("date")["value"])

# Rolling averages and variation
filtered_df["rolling_3m"] = filtered_df["value"].rolling(window=3).mean()
filtered_df["rolling_6m"] = filtered_df["value"].rolling(window=6).mean()
filtered_df["monthly_variation"] = filtered_df["value"].pct_change() * 100

st.subheader("Monthly Variation and Moving Averages")
st.line_chart(filtered_df.set_index("date")[["value", "rolling_3m", "rolling_6m"]])

# Table
st.subheader("Filtered Data")
st.dataframe(filtered_df.reset_index(drop=True))

# Export
st.download_button(
    label="📥 Download filtered data as CSV",
    data=filtered_df.to_csv(index=False),
    file_name=f"{table_name}_filtered.csv",
    mime="text/csv"
)