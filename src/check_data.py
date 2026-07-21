import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

tables = [
    "companies",
    "financial_ratios",
    "market_cap",
    "stock_prices"
]

for table in tables:
    print("\n" + "=" * 40)
    print(table)

    df = pd.read_sql(
        f"SELECT * FROM {table} LIMIT 5",
        conn
    )

    print(df)

conn.close()