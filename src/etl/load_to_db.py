import os
import sqlite3
import pandas as pd

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

DB_PATH = os.path.join(BASE_DIR, "db", "nifty100.db")

DATASET_DIR = os.path.join(BASE_DIR, "Data Sets")
SUPPORTING_DIR = os.path.join(BASE_DIR, "Supporting datasets")


FILES = {
    "companies": (
        os.path.join(DATASET_DIR, "companies.xlsx"),
        1
    ),
    "profitandloss": (
        os.path.join(DATASET_DIR, "profitandloss.xlsx"),
        1
    ),
    "balancesheet": (
        os.path.join(DATASET_DIR, "balancesheet.xlsx"),
        1
    ),
    "cashflow": (
        os.path.join(DATASET_DIR, "cashflow.xlsx"),
        1
    ),
    "analysis": (
        os.path.join(DATASET_DIR, "analysis.xlsx"),
        1
    ),
    "documents": (
        os.path.join(DATASET_DIR, "documents.xlsx"),
        1
    ),
    "prosandcons": (
        os.path.join(DATASET_DIR, "prosandcons.xlsx"),
        1
    ),
    "financial_ratios": (
        os.path.join(SUPPORTING_DIR, "financial_ratios.xlsx"),
        0
    ),
    "market_cap": (
        os.path.join(SUPPORTING_DIR, "market_cap.xlsx"),
        0
    ),
    "peer_groups": (
        os.path.join(SUPPORTING_DIR, "peer_groups.xlsx"),
        0
    ),
    "sectors": (
        os.path.join(SUPPORTING_DIR, "sectors.xlsx"),
        0
    ),
    "stock_prices": (
        os.path.join(SUPPORTING_DIR, "stock_prices.xlsx"),
        0
    )
}


conn = sqlite3.connect(DB_PATH)

audit = []

for table, (path, header) in FILES.items():

    print(f"Loading {table}...")

    df = pd.read_excel(path, header=header)

    df.columns = [
        str(c).strip().lower().replace(" ", "_")
        for c in df.columns
    ]

    df.to_sql(
        table,
        conn,
        if_exists="append",
        index=False
    )

    audit.append({
        "table": table,
        "rows_loaded": len(df)
    })

conn.commit()

audit_df = pd.DataFrame(audit)

output_dir = os.path.join(BASE_DIR, "output")
os.makedirs(output_dir, exist_ok=True)

audit_df.to_csv(
    os.path.join(output_dir, "load_audit.csv"),
    index=False
)

conn.close()

print("\nAll datasets loaded successfully!")
print(audit_df)