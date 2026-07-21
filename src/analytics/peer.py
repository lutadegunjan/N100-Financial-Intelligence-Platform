import sqlite3
import pandas as pd
import os


DB_PATH = "db/nifty100.db"
PEER_FILE = "config/peer_groups.xlsx"


def load_peer_groups():

    if not os.path.exists(PEER_FILE):
        raise FileNotFoundError(
            "peer_groups.xlsx not found in config folder"
        )

    peer_df = pd.read_excel(
        PEER_FILE
    )

    return peer_df



def load_financial_data():

    conn = sqlite3.connect(
        DB_PATH
    )


    query = """
    SELECT
        company_id,
        year,

        return_on_equity_pct,
        return_on_capital_employed_pct,
        net_profit_margin_pct,

        debt_to_equity,
        free_cash_flow_cr,

        pat_cagr_5yr,
        revenue_cagr_5yr,
        eps_cagr_5yr,

        interest_coverage,
        asset_turnover

    FROM financial_ratios
    """


    df = pd.read_sql(
        query,
        conn
    )


    conn.close()


    # latest year per company

    df = (
        df
        .sort_values("year")
        .groupby("company_id")
        .tail(1)
    )


    return df




def calculate_percentile(
        group,
        metric
):

    temp = group.copy()


    # lower debt is better
    if metric == "Debt Equity":

        temp["percentile_rank"] = (
            1 -
            temp["value"]
            .rank(
                pct=True,
                method="min"
            )
        )

    else:

        temp["percentile_rank"] = (
            temp["value"]
            .rank(
                pct=True,
                method="min"
            )
        )


    return temp




def create_peer_percentiles():


    peer_groups = load_peer_groups()

    financial = load_financial_data()



    print(
        "Companies with peer groups:",
        peer_groups["company_id"].nunique()
    )


    merged = financial.merge(
        peer_groups,
        on="company_id",
        how="inner"
    )


    print("\nPeer Groups:")

    print(
        merged["peer_group_name"]
        .value_counts()
    )


    metrics = {

        "ROE":
            "return_on_equity_pct",

        "ROCE":
            "return_on_capital_employed_pct",

        "Net Profit Margin":
            "net_profit_margin_pct",

        "Debt Equity":
            "debt_to_equity",

        "FCF":
            "free_cash_flow_cr",

        "PAT CAGR 5Y":
            "pat_cagr_5yr",

        "Revenue CAGR 5Y":
            "revenue_cagr_5yr",

        "EPS CAGR 5Y":
            "eps_cagr_5yr",

        "Interest Coverage":
            "interest_coverage",

        "Asset Turnover":
            "asset_turnover"
    }



    results = []


    for peer_group in merged["peer_group_name"].unique():

        peer_data = merged[
            merged["peer_group_name"]
            ==
            peer_group
        ]


        for metric_name, column in metrics.items():

            temp = peer_data[
                [
                    "company_id",
                    "year",
                    column
                ]
            ].copy()


            temp = temp.rename(
                columns={
                    column:"value"
                }
            )


            # remove missing values

            temp = temp.dropna(
                subset=[
                    "value"
                ]
            )


            if len(temp)==0:
                continue



            temp = calculate_percentile(
                temp,
                metric_name
            )


            temp["peer_group_name"] = peer_group

            temp["metric"] = metric_name


            results.append(
                temp[
                    [
                        "company_id",
                        "peer_group_name",
                        "metric",
                        "value",
                        "percentile_rank",
                        "year"
                    ]
                ]
            )



    if len(results)==0:

        print(
            "No peer percentile data generated"
        )

        return



    final = pd.concat(
        results,
        ignore_index=True
    )



    conn = sqlite3.connect(
        DB_PATH
    )


    cursor = conn.cursor()


    cursor.execute(
        """
        DELETE FROM peer_percentiles
        """
    )


    final.to_sql(
        "peer_percentiles",
        conn,
        if_exists="append",
        index=False
    )


    conn.commit()

    conn.close()



    print(
        "\nPeer percentile calculation completed."
    )

    print(
        "Rows inserted:",
        len(final)
    )




if __name__ == "__main__":

    create_peer_percentiles()