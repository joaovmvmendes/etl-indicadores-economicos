
# 📈 Economic Indicators ETL & Dashboard

This project performs an **automated ETL pipeline** to collect, transform, store, and visualize economic indicators from the Central Bank of Brazil (BCB) using Python.

The pipeline supports:
- **IPCA** (Inflation)
- **SELIC** (Interest Rate)
- **USD/BRL Exchange Rate**

It uses public APIs, performs transformations, loads data into PostgreSQL, and provides an interactive dashboard built with Streamlit.

---

## 🧱 Project Structure

```
etl-indicadores-economicos/
├── etl/
│   ├── extract.py        # Extracts data from BCB API
│   ├── transform.py      # Cleans and standardizes data
│   └── load.py           # Loads data into PostgreSQL
├── dashboard/
│   └── app.py            # Streamlit dashboard application
├── data/                 # Stores CSVs (raw and cleaned)
├── requirements.txt
└── README.md
```

---

## ⚙️ Requirements

- Python 3.9+
- PostgreSQL
- pip (Python package manager)

---

## 🚀 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/etl-indicadores-economicos.git
cd etl-indicadores-economicos
```

### 2. Create and activate virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # or 'source .venv/bin/activate.fish' or '.venv\Scripts\activate' on Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Ensure PostgreSQL is running and accessible. Default configuration used:

```
host=localhost
port=5432
database=economic_data
user=etl_user
password=123456
```

Create the database and user if not already set.

### 5. Run the ETL pipeline

#### Extract

```bash
python etl/extract.py
```

#### Transform

```bash
python etl/transform.py
```

#### Load

```bash
python etl/load.py
```

### 6. Launch the dashboard

```bash
streamlit run dashboard/app.py
```

The dashboard will be available at: `http://localhost:8501`

---

## 📊 Features

- Date range filter
- Multiple indicators (IPCA, SELIC, USD)
- Rolling averages (3M, 6M)
- Monthly variation %
- CSV export button
- PostgreSQL backend for persistence

---

## 📌 Notes

- All code is internationalized and documented in English.
- Fully modular, reusable ETL scripts.
- Clean architecture and log tracing for each stage.

---

## 📚 License

MIT License.
