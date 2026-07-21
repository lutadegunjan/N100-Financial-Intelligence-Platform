import sqlite3
import pandas as pd

print("Script started")

conn = sqlite3.connect("db/nifty100.db")

df = pd.read_sql("SELECT * FROM profitandloss LIMIT 5;", conn)

print("\nColumns:")
print(df.columns.tolist())

print("\nSample Data:")
print(df)

conn.close()

print("Script finished")