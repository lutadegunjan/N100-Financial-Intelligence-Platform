import sqlite3
import pandas as pd


DB_PATH = "db/nifty100.db"

conn = sqlite3.connect(DB_PATH)


queries = {

"Top 10 Companies by Market Cap":

"""
SELECT 
company_id,
year,
market_cap_crore
FROM market_cap
WHERE year = (
    SELECT MAX(year)
    FROM market_cap
)
ORDER BY market_cap_crore DESC
LIMIT 10;
""",


"Highest ROE Companies":

"""
SELECT
company_name,
roe_percentage
FROM companies
ORDER BY roe_percentage DESC
LIMIT 10;
""",


"Highest Dividend Yield":

"""
SELECT
company_id,
year,
dividend_yield_pct
FROM market_cap
ORDER BY dividend_yield_pct DESC
LIMIT 10;
""",


"Companies with Highest Cash Flow":

"""
SELECT
company_id,
year,
cash_from_operations_cr
FROM financial_ratios
ORDER BY cash_from_operations_cr DESC
LIMIT 10;
"""

}


for name, query in queries.items():

    print("\n" + "="*50)
    print(name)

    df = pd.read_sql(query, conn)

    print(df)


conn.close()
