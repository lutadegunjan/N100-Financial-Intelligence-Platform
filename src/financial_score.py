import os
import sqlite3
import pandas as pd


# -----------------------------
# Paths
# -----------------------------

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

DB_PATH = os.path.join(BASE_DIR, "db", "nifty100.db")

OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# -----------------------------
# Load Data
# -----------------------------

conn = sqlite3.connect(DB_PATH)

companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

market = pd.read_sql(
    "SELECT * FROM market_cap",
    conn
)

conn.close()

# -----------------------------
# Prepare Company Identifier
# -----------------------------

if "company_id" not in companies.columns:
    companies = companies.rename(
        columns={"id": "company_id"}
    )
# -----------------------------
# Latest Financial Data
# -----------------------------

latest_ratios = (
    ratios.sort_values("year")
    .groupby("company_id")
    .tail(1)
)

latest_market = (
    market.sort_values("year")
    .groupby("company_id")
    .tail(1)
)


# -----------------------------
# Merge
# -----------------------------

df = companies.merge(
    latest_ratios,
    on="company_id",
    how="left"
)

df = df.merge(
    latest_market,
    on="company_id",
    how="left",
    suffixes=("", "_market")
)


df["financial_score"] = 0


# -----------------------------
# Quality Factors
# -----------------------------

# ROE - 20%
if "return_on_equity_pct" in df:
    df["financial_score"] += (
        df["return_on_equity_pct"]
        .clip(0, 50)
        .fillna(0)
        * 0.20
    )


# ROCE - 15%
if "return_on_capital_employed_pct" in df:
    df["financial_score"] += (
        df["return_on_capital_employed_pct"]
        .clip(0, 50)
        .fillna(0)
        * 0.15
    )


# ROA - 10%
if "return_on_assets_pct" in df:
    df["financial_score"] += (
        df["return_on_assets_pct"]
        .clip(0, 30)
        .fillna(0)
        * 0.10
    )


# Profitability - 20%
if "net_profit_margin_pct" in df:
    df["financial_score"] += (
        df["net_profit_margin_pct"]
        .clip(0, 50)
        .fillna(0)
        * 0.20
    )


# Growth - 15%
growth_score = 0

if "revenue_cagr_5yr" in df:
    growth_score += (
        df["revenue_cagr_5yr"]
        .clip(0, 30)
        .fillna(0)
        * 0.5
    )

if "pat_cagr_5yr" in df:
    growth_score += (
        df["pat_cagr_5yr"]
        .clip(0, 30)
        .fillna(0)
        * 0.5
    )

df["financial_score"] += growth_score * 0.15


# Debt Health - 10%
if "debt_to_equity" in df:

    debt_score = (
        1 /
        (1 + df["debt_to_equity"].fillna(10))
    ) * 100

    df["financial_score"] += (
        debt_score * 0.10
    )


# Cash Flow - 10%
if "cash_from_operations_cr" in df:

    cash_score = (
        df["cash_from_operations_cr"]
        .rank(pct=True)
        * 100
    )

    df["financial_score"] += (
        cash_score.fillna(0)
        * 0.10
    )


# -----------------------------
# Rating
# -----------------------------

def rating(score):

    if score >= 75:
        return "Excellent"

    elif score >= 55:
        return "Strong"

    elif score >= 35:
        return "Average"

    else:
        return "Weak"

# Normalize score to 100 scale

max_score = df["financial_score"].max()

if max_score > 0:
    df["financial_score"] = (
        df["financial_score"] / max_score
    ) * 100
df["rating"] = df["financial_score"].apply(rating)


# -----------------------------
# Save Output
# -----------------------------

df = df.sort_values(
    "financial_score",
    ascending=False
)


output_file = os.path.join(
    OUTPUT_DIR,
    "financial_scorecard.csv"
)

df.to_csv(
    output_file,
    index=False
)


print(
    df[
        [
            "company_name",
            "financial_score",
            "rating"
        ]
    ].head(20)
)


print("\nFinancial Scorecard Generated Successfully!")
print("Saved at:", output_file)