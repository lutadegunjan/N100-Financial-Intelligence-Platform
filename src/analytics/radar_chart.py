"""
N100 Financial Intelligence Platform
Sprint 3 - Day 19
Peer Radar Chart Generator
"""

import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


DB_PATH = "db/nifty100.db"

OUTPUT_DIR = "reports/radar_charts"


METRICS = [
    "return_on_equity_pct",
    "return_on_capital_employed_pct",
    "net_profit_margin_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "pat_cagr_5yr",
    "revenue_cagr_5yr",
    "composite_quality_score"
]


DISPLAY_NAMES = [
    "ROE",
    "ROCE",
    "NPM",
    "D/E",
    "FCF",
    "PAT CAGR",
    "Revenue CAGR",
    "Score"
]


def load_data():

    conn = sqlite3.connect(DB_PATH)


    ratios = pd.read_sql(
        """
        SELECT *
        FROM financial_ratios
        """,
        conn
    )


    companies = pd.read_sql(
        """
        SELECT id, company_name
        FROM companies
        """,
        conn
    )


    peers = pd.read_sql(
        """
        SELECT company_id, peer_group_name
        FROM peer_groups
        """,
        conn
    )


    conn.close()


    ratios = (
        ratios
        .sort_values("year")
        .groupby("company_id")
        .tail(1)
    )


    df = ratios.merge(
        companies,
        left_on="company_id",
        right_on="id",
        how="left"
    )


    df = df.merge(
        peers,
        on="company_id",
        how="left"
    )


    return df



def normalize(value, series):

    series = series.dropna()


    if value is None or pd.isna(value):
        return 0


    if len(series) == 0:
        return 0


    if series.max() == series.min():
        return 50


    score = (
        (value - series.min())
        /
        (series.max() - series.min())
    ) * 100


    return max(
        0,
        min(
            100,
            score
        )
    )



def create_radar(company_row, peer_data):

    company_name = company_row["company_name"]


    values = []

    averages = []


    for metric in METRICS:

        peer_series = peer_data[metric]


        company_value = company_row[metric]


        values.append(
            normalize(
                company_value,
                peer_series
            )
        )


        peer_average = peer_series.mean()


        averages.append(
            normalize(
                peer_average,
                peer_series
            )
        )


    values.append(values[0])
    averages.append(averages[0])


    angles = np.linspace(
        0,
        2*np.pi,
        len(values)
    )


    fig = plt.figure(
        figsize=(7,7)
    )


    ax = plt.subplot(
        polar=True
    )


    ax.plot(
        angles,
        values,
        linewidth=2
    )


    ax.fill(
        angles,
        values,
        alpha=0.25
    )


    ax.plot(
        angles,
        averages,
        linestyle="--",
        linewidth=2
    )


    ax.set_xticks(
        angles[:-1]
    )


    ax.set_xticklabels(
        DISPLAY_NAMES,
        fontsize=9
    )


    ax.set_ylim(
        0,
        100
    )


    ax.set_title(
        company_name,
        fontsize=14
    )


    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )


    filename = (
        company_name
        .replace("\n", " ")
        .replace("/", "_")
        .replace(" ", "_")
        +
        "_radar.png"
    )


    filepath = os.path.join(
        OUTPUT_DIR,
        filename
    )


    plt.savefig(
        filepath,
        bbox_inches="tight"
    )


    plt.close()


    print(
        "Created:",
        filepath
    )



def generate_all():

    df = load_data()


    created = 0


    for _, row in df.iterrows():


        peer_group = row["peer_group_name"]


        if pd.isna(peer_group):
            continue



        peers = df[
            df["peer_group_name"]
            ==
            peer_group
        ]



        create_radar(
            row,
            peers
        )


        created += 1



    print(
        "Radar charts generated:",
        created
    )



if __name__ == "__main__":

    generate_all()