import sqlite3

DB_PATH = "db/nifty100.db"

NEW_COLUMNS = [
    ("return_on_capital_employed_pct", "REAL"),
    ("return_on_assets_pct", "REAL"),
    ("net_debt_cr", "REAL"),
    ("revenue_cagr_3yr", "REAL"),
    ("revenue_cagr_5yr", "REAL"),
    ("revenue_cagr_10yr", "REAL"),
    ("pat_cagr_3yr", "REAL"),
    ("pat_cagr_5yr", "REAL"),
    ("pat_cagr_10yr", "REAL"),
    ("eps_cagr_3yr", "REAL"),
    ("eps_cagr_5yr", "REAL"),
    ("eps_cagr_10yr", "REAL"),
    ("composite_quality_score", "REAL"),
    ("high_leverage_flag", "INTEGER"),
    ("icr_label", "TEXT"),
]

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

existing = [
    row[1]
    for row in cur.execute("PRAGMA table_info(financial_ratios)")
]

for column_name, column_type in NEW_COLUMNS:
    if column_name not in existing:
        sql = (
            f"ALTER TABLE financial_ratios "
            f"ADD COLUMN {column_name} {column_type}"
        )
        cur.execute(sql)
        print(f"Added {column_name}")
    else:
        print(f"Already exists: {column_name}")

conn.commit()
conn.close()

print("\nSchema updated successfully.")