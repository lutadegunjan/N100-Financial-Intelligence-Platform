import sqlite3
import pandas as pd
import os

from etl.validator import DataValidator


DB_PATH = "db/nifty100.db"

OUTPUT_PATH = "output/data_quality_report.csv"


conn = sqlite3.connect(DB_PATH)


validator = DataValidator()


# ----------------------------
# Load tables
# ----------------------------

companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

financial_ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

market_cap = pd.read_sql(
    "SELECT * FROM market_cap",
    conn
)

stock_prices = pd.read_sql(
    "SELECT * FROM stock_prices",
    conn
)


# ----------------------------
# DQ-01 Primary Key Checks
# ----------------------------

validator.dq01_primary_key(
    companies,
    "id",
    "companies"
)


validator.dq01_primary_key(
    financial_ratios,
    "id",
    "financial_ratios"
)


# ----------------------------
# DQ-02 Mandatory Fields
# ----------------------------

validator.dq02_mandatory_fields(
    companies,
    ["id", "company_name"],
    "companies"
)


validator.dq02_mandatory_fields(
    stock_prices,
    ["company_id", "date", "close_price"],
    "stock_prices"
)


# ----------------------------
# DQ-04 Duplicate Records
# ----------------------------

validator.dq04_duplicate_records(
    companies,
    "companies"
)


validator.dq04_duplicate_records(
    stock_prices,
    "stock_prices"
)


# ----------------------------
# DQ-05 Negative Values
# ----------------------------

validator.dq05_non_negative_values(
    market_cap,
    "market_cap_crore",
    "market_cap"
)


# ----------------------------
# Export Report
# ----------------------------

os.makedirs("output", exist_ok=True)

validator.export_failures(
    OUTPUT_PATH
)


conn.close()


print("Data Quality Validation Completed!")
print(f"Report saved at: {OUTPUT_PATH}")