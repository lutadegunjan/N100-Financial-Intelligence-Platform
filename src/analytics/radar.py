"""
Peer Radar Chart Generator
Sprint 3 - Day 19
"""

import sqlite3
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


DB_PATH = "db/nifty100.db"

OUTPUT_DIR = "reports/radar_charts"



METRICS = {
    "return_on_equity_pct": "ROE",
    "return_on_capital_employed_pct": "ROCE",
    "net_profit_margin_pct": "NPM",
    "debt_to_equity": "D/E",
    "free_cash_flow_cr": "FCF",
    "pat_cagr_5yr": "PAT CAGR",
    "revenue_cagr_5yr": "Revenue CAGR",
    "composite_quality_score": "Score"
}



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
        SELECT
            id AS company_id,
            company_name
        FROM companies
        """,
        conn
    )


    peers = pd.read_excel(
        "config/peer_groups.xlsx"
    )


    df = (
        ratios
        .sort_values("year")
        .groupby("company_id")
        .tail(1)
    )


    df = df.merge(
        companies,
        on="company_id",
        how="left"
    )


    df = df.merge(
        peers,
        on="company_id",
        how="left"
    )


    return df



def normalize(values):

    values = values.fillna(0)

    minimum = values.min()
    maximum = values.max()


    if maximum == minimum:
        return values * 0 + 50


    return (
        (values - minimum)
        /
        (maximum - minimum)
        *
        100
    )



def create_radar(company, data):

    labels = list(
        METRICS.values()
    )


    company_values = []


    for column in METRICS:

        company_values.append(
            data[column]
            .iloc[0]
        )


    peer_avg = (
        data[
            list(METRICS.keys())
        ]
        .mean()
        .tolist()
    )


    company_values = normalize(
        pd.Series(company_values)
    ).tolist()


    peer_avg = normalize(
        pd.Series(peer_avg)
    ).tolist()



    angles = np.linspace(
        0,
        2*np.pi,
        len(labels),
        endpoint=False
    )


    company_values += company_values[:1]
    peer_avg += peer_avg[:1]
    angles = np.append(
        angles,
        angles[0]
    )


    fig = plt.figure(
        figsize=(7,7)
    )


    ax = plt.subplot(
        111,
        polar=True
    )


    ax.plot(
        angles,
        company_values
    )

    ax.fill(
        angles,
        company_values,
        alpha=0.25
    )


    ax.plot(
        angles,
        peer_avg,
        linestyle="--"
    )


    ax.set_xticks(
        angles[:-1]
    )


    ax.set_xticklabels(
        labels,
        fontsize=9
    )


    ax.set_title(
        company,
        fontsize=14
    )


    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )


    filename = (
        company
        .replace(" ","_")
        +
        "_radar.png"
    )


    path = os.path.join(
        OUTPUT_DIR,
        filename
    )


    plt.savefig(
        path,
        bbox_inches="tight"
    )


    plt.close()



def generate_all():

    df = load_data()


    count = 0


    for company in df["company_name"].dropna().unique():


        company_data = df[
            df["company_name"] == company
        ]


        peer_group = (
            company_data["peer_group_name"]
            .iloc[0]
        )


        peer_data = df[
            df["peer_group_name"]
            ==
            peer_group
        ]


        create_radar(
            company,
            peer_data
        )


        count += 1



    print(
        "Radar charts generated:",
        count
    )



if __name__ == "__main__":
    generate_all()