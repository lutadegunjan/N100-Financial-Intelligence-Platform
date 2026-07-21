import sqlite3
import pandas as pd
import os


DB_PATH = "db/nifty100.db"
OUTPUT = "config/peer_groups.xlsx"


PEER_MAPPING = {

    # IT Services
    "HCLTECH": "IT Services",
    "INFY": "IT Services",
    "LTIM": "IT Services",
    "TCS": "IT Services",
    "TECHM": "IT Services",


    # Banking & Financial Services
    "AXISBANK": "Banking & Financial Services",
    "BANKBARODA": "Banking & Financial Services",
    "CANBK": "Banking & Financial Services",
    "HDFCBANK": "Banking & Financial Services",
    "ICICIBANK": "Banking & Financial Services",
    "INDUSINDBK": "Banking & Financial Services",
    "KOTAKBANK": "Banking & Financial Services",
    "PNB": "Banking & Financial Services",
    "SBIN": "Banking & Financial Services",

    "BAJAJFINSV": "Banking & Financial Services",
    "BAJAJHLDNG": "Banking & Financial Services",
    "BAJFINANCE": "Banking & Financial Services",
    "CHOLAFIN": "Banking & Financial Services",
    "HDFCLIFE": "Banking & Financial Services",
    "ICICIGI": "Banking & Financial Services",
    "ICICIPRULI": "Banking & Financial Services",
    "JIOFIN": "Banking & Financial Services",
    "LICI": "Banking & Financial Services",
    "PFC": "Banking & Financial Services",
    "RECLTD": "Banking & Financial Services",
    "SBILIFE": "Banking & Financial Services",
    "SHRIRAMFIN": "Banking & Financial Services",
    "IRFC": "Banking & Financial Services",


    # FMCG
    "BRITANNIA": "FMCG",
    "DABUR": "FMCG",
    "GODREJCP": "FMCG",
    "HINDUNILVR": "FMCG",
    "ITC": "FMCG",
    "NESTLEIND": "FMCG",
    "TATACONSUM": "FMCG",


    # Auto
    "BAJAJ-AUTO": "Auto",
    "EICHERMOT": "Auto",
    "HEROMOTOCO": "Auto",
    "M&M": "Auto",
    "MARUTI": "Auto",
    "MOTHERSON": "Auto",
    "TATAMOTORS": "Auto",
    "TVSMOTOR": "Auto",


    # Pharmaceuticals
    "ABB": "Pharmaceuticals",
    "CIPLA": "Pharmaceuticals",
    "DIVISLAB": "Pharmaceuticals",
    "DRREDDY": "Pharmaceuticals",
    "SUNPHARMA": "Pharmaceuticals",
    "TORNTPHARM": "Pharmaceuticals",


    # Energy
    "ADANIENSOL": "Energy",
    "ADANIGREEN": "Energy",
    "ADANIPOWER": "Energy",
    "ATGL": "Energy",
    "BPCL": "Energy",
    "GAIL": "Energy",
    "IOC": "Energy",
    "NTPC": "Energy",
    "ONGC": "Energy",
    "RELIANCE": "Energy",
    "TATAPOWER": "Energy",


    # Metals
    "COALINDIA": "Metals & Mining",
    "HINDALCO": "Metals & Mining",
    "JINDALSTEL": "Metals & Mining",
    "JSWSTEEL": "Metals & Mining",
    "TATASTEEL": "Metals & Mining",


    # Infrastructure
    "ADANIENT": "Infrastructure & Construction",
    "ADANIPORTS": "Infrastructure & Construction",
    "DLF": "Infrastructure & Construction",
    "LODHA": "Infrastructure & Construction",
    "LT": "Infrastructure & Construction",


    # Consumer Durables
    "ASIANPAINT": "Consumer Durables",
    "BOSCHLTD": "Consumer Durables",
    "DMART": "Consumer Durables",
    "HAVELLS": "Consumer Durables",
    "PIDILITIND": "Consumer Durables",
    "TITAN": "Consumer Durables",
    "TRENT": "Consumer Durables",


    # Healthcare
    "APOLLOHOSP": "Healthcare",


    # Industrials
    "BEL": "Industrials",
    "BHEL": "Industrials",
    "HAL": "Industrials",
    "SIEMENS": "Industrials",


    # Telecom / Transport
    "BHARTIARTL": "Telecom & Media",
    "NAUKRI": "Telecom & Media",
    "INDIGO": "Transport",
    "IRCTC": "Transport",


    # Utilities
    "AMBUJACEM": "Utilities",
    "GRASIM": "Utilities",
    "JSWENERGY": "Utilities",
    "NHPC": "Utilities",
    "POWERGRID": "Utilities",
    "SHREECEM": "Utilities"
}



def create_file():

    conn = sqlite3.connect(DB_PATH)

    companies = pd.read_sql(
        """
        SELECT
            id AS company_id,
            company_name
        FROM companies
        """,
        conn
    )


    companies["peer_group_name"] = (
        companies["company_id"]
        .map(PEER_MAPPING)
    )


    missing = companies[
        companies["peer_group_name"].isna()
    ]


    if len(missing) > 0:
        print("Companies without peer group:")
        print(
            missing[
                ["company_id", "company_name"]
            ]
        )


    companies = companies.dropna()


    os.makedirs(
        "config",
        exist_ok=True
    )


    companies.to_excel(
        OUTPUT,
        index=False
    )


    print("Created:", OUTPUT)
    print("Rows:", len(companies))



if __name__ == "__main__":
    create_file()