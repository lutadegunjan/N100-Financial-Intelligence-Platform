import sqlite3
import pandas as pd


DB_PATH = "db/nifty100.db"


def calculate_cagr(start_value, end_value, years):

    if (
        pd.isna(start_value)
        or pd.isna(end_value)
        or start_value <= 0
        or end_value <= 0
    ):
        return None

    return (
        ((end_value / start_value) ** (1 / years)) - 1
    ) * 100



def update_cagr():

    conn = sqlite3.connect(DB_PATH)


    df = pd.read_sql(
        """
        SELECT
            company_id,
            year,
            sales,
            net_profit

        FROM profitandloss

        ORDER BY company_id, year
        """,
        conn
    )


    updated = 0


    for company_id, group in df.groupby("company_id"):


        group = (
            group
            .sort_values("year")
            .reset_index(drop=True)
        )


        latest = group.iloc[-1]


        revenue_3 = None
        revenue_5 = None
        pat_3 = None
        pat_5 = None



        if len(group) >= 4:

            old = group.iloc[-4]

            revenue_3 = calculate_cagr(
                old["sales"],
                latest["sales"],
                3
            )

            pat_3 = calculate_cagr(
                old["net_profit"],
                latest["net_profit"],
                3
            )



        if len(group) >= 6:

            old = group.iloc[-6]

            revenue_5 = calculate_cagr(
                old["sales"],
                latest["sales"],
                5
            )

            pat_5 = calculate_cagr(
                old["net_profit"],
                latest["net_profit"],
                5
            )



        cursor = conn.execute(
            """
            UPDATE financial_ratios

            SET
                revenue_cagr_3yr = ?,
                revenue_cagr_5yr = ?,
                pat_cagr_3yr = ?,
                pat_cagr_5yr = ?

            WHERE company_id = ?

            """,
            (
                revenue_3,
                revenue_5,
                pat_3,
                pat_5,
                company_id
            )
        )


        updated += cursor.rowcount



    conn.commit()
    conn.close()


    print(
        "CAGR update completed."
    )

    print(
        "Rows updated:",
        updated
    )



if __name__ == "__main__":

    update_cagr()