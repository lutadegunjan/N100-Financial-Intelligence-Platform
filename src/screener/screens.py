import sqlite3
import pandas as pd
import os


DB_PATH = "db/nifty100.db"


OUTPUT_DIR = "output"



def load_data():

    conn = sqlite3.connect(DB_PATH)


    # Financial ratios
    financial = pd.read_sql(
        """
        SELECT *
        FROM financial_ratios
        """,
        conn
    )


    # Latest financial year
    financial = (
        financial
        .sort_values("year")
        .groupby("company_id")
        .tail(1)
    )


    # Market data
    market = pd.read_sql(
        """
        SELECT company_id,
               pe_ratio,
               pb_ratio,
               dividend_yield_pct
        FROM market_cap
        """,
        conn
    )


    # Latest market data
    market = (
        market
        .drop_duplicates(
            subset=["company_id"],
            keep="last"
        )
    )


    # Company names
    companies = pd.read_sql(
        """
        SELECT id,
               company_name
        FROM companies
        """,
        conn
    )


    df = financial.merge(
        market,
        on="company_id",
        how="left"
    )


    df = df.merge(
        companies,
        left_on="company_id",
        right_on="id",
        how="left"
    )


    # Clean names
    df["company_name"] = (
        df["company_name"]
        .astype(str)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )


    return df




def quality_growth_screen(df):

    result = df[
        (df["return_on_equity_pct"] > 15) &
        (df["revenue_cagr_5yr"] > 10) &
        (df["pat_cagr_5yr"] > 10) &
        (df["debt_to_equity"] < 1)
    ]


    return result




def value_screen(df):

    result = df[
        (df["pe_ratio"] < 25) &
        (df["pb_ratio"] < 5) &
        (df["return_on_equity_pct"] > 12)
    ]


    return result




def dividend_screen(df):

    result = df[
        (df["dividend_yield_pct"] > 1) &
        (df["return_on_equity_pct"] > 10)
    ]


    return result




def save_screen(result, filename):

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )


    path = os.path.join(
        OUTPUT_DIR,
        filename
    )


    result.to_csv(
        path,
        index=False
    )


    print(
        f"Saved {filename}: {len(result)} companies"
    )




def run_screens():


    df = load_data()


    print(
        "Total companies loaded:",
        len(df)
    )


    quality = quality_growth_screen(df)

    value = value_screen(df)

    dividend = dividend_screen(df)



    save_screen(
        quality,
        "quality_growth_screen.csv"
    )


    save_screen(
        value,
        "value_screen.csv"
    )


    save_screen(
        dividend,
        "dividend_screen.csv"
    )



    print("\nQuality Growth Top Companies:")

    print(
        quality[
            ["company_name",
             "return_on_equity_pct",
             "revenue_cagr_5yr",
             "pat_cagr_5yr"]
        ]
        .head(10)
    )



    print("\nValue Screen Top Companies:")

    print(
        value[
            ["company_name",
             "pe_ratio",
             "pb_ratio",
             "return_on_equity_pct"]
        ]
        .head(10)
    )



    print("\nDividend Screen Top Companies:")

    print(
        dividend[
            ["company_name",
             "dividend_yield_pct",
             "return_on_equity_pct"]
        ]
        .head(10)
    )




if __name__ == "__main__":

    run_screens()