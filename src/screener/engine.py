import sqlite3
import pandas as pd
import yaml
import os


DB_PATH = "db/nifty100.db"
CONFIG_PATH = "config/screener_config.yaml"
OUTPUT_PATH = "output/screener_results.csv"



def load_config():

    with open(CONFIG_PATH, "r") as file:
        return yaml.safe_load(file)["filters"]



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


    # Latest financial year per company
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
               year,
               market_cap_crore,
               pe_ratio,
               pb_ratio,
               dividend_yield_pct
        FROM market_cap
        """,
        conn
    )


    # Latest market year
    market = (
        market
        .sort_values("year")
        .groupby("company_id")
        .tail(1)
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


    # Merge financial + market
    df = financial.merge(
        market,
        on="company_id",
        how="left"
    )


    # Merge company details
    df = df.merge(
        companies,
        left_on="company_id",
        right_on="id",
        how="left"
    )


    # Clean company names
    df["company_name"] = (
        df["company_name"]
        .astype(str)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )


    return df




def calculate_score(df):

    df["score"] = 0


    # Profitability
    if "return_on_equity_pct" in df.columns:

        df.loc[
            df["return_on_equity_pct"] > 15,
            "score"
        ] += 20



    # Debt quality
    if "debt_to_equity" in df.columns:

        df.loc[
            df["debt_to_equity"] < 1,
            "score"
        ] += 15



    # Revenue growth
    if "revenue_cagr_5yr" in df.columns:

        df.loc[
            df["revenue_cagr_5yr"] > 10,
            "score"
        ] += 15



    # Profit growth
    if "pat_cagr_5yr" in df.columns:

        df.loc[
            df["pat_cagr_5yr"] > 10,
            "score"
        ] += 15



    # Valuation
    if "pe_ratio" in df.columns:

        df.loc[
            df["pe_ratio"] < 25,
            "score"
        ] += 15



    if "pb_ratio" in df.columns:

        df.loc[
            df["pb_ratio"] < 5,
            "score"
        ] += 10



    # Dividend
    if "dividend_yield_pct" in df.columns:

        df.loc[
            df["dividend_yield_pct"] > 1,
            "score"
        ] += 10



    return df




def apply_filters(df, filters):

    # Remove companies without names
    df = df.dropna(
        subset=["company_name"]
    )


    return df




def run_screener():

    filters = load_config()


    df = load_data()


    print(
        "Total companies before scoring:",
        len(df)
    )


    print("\nCompany name check:")
    print(
        df["company_name"]
        .head(10)
        .to_list()
    )


    df = apply_filters(
        df,
        filters
    )


    df = calculate_score(df)


    df = df.sort_values(
        "score",
        ascending=False
    )


    os.makedirs(
        "output",
        exist_ok=True
    )


    df.to_csv(
        OUTPUT_PATH,
        index=False
    )


    return df




if __name__ == "__main__":


    result = run_screener()


    print("\nTop Screened Companies:\n")


    print(
        result[
            [
                "company_name",
                "return_on_equity_pct",
                "debt_to_equity",
                "score"
            ]
        ]
        .head(20)
    )


    print(
        "\nCompanies ranked:",
        len(result)
    )


    print(
        "\nSaved:",
        OUTPUT_PATH
    )