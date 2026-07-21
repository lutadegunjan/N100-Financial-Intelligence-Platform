import sqlite3
import pandas as pd
import os


DB_PATH = "db/nifty100.db"

OUTPUT_PATH = "output/peer_comparison.csv"



def load_data():

    conn = sqlite3.connect(DB_PATH)


    financial = pd.read_sql(
        """
        SELECT *
        FROM financial_ratios
        """,
        conn
    )


    financial = (
        financial
        .sort_values("year")
        .groupby("company_id")
        .tail(1)
    )


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


    market = (
        market
        .drop_duplicates(
            subset=["company_id"],
            keep="last"
        )
    )


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


    # Clean company names

    df["company_name"] = (
        df["company_name"]
        .astype(str)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )


    return df




def peer_compare(company_name):


    df = load_data()


    company_name = company_name.strip()



    company = df[
        df["company_name"]
        .str.contains(
            company_name,
            case=False,
            na=False,
            regex=False
        )
    ]



    if company.empty:

        print(
            "\nCompany not found."
        )

        print(
            "Try names like: Trent, Infosys, Reliance"
        )

        return



    company_row = company.iloc[0]



    metrics = [

        "return_on_equity_pct",

        "debt_to_equity",

        "revenue_cagr_5yr",

        "pat_cagr_5yr",

        "pe_ratio",

        "pb_ratio",

        "dividend_yield_pct"

    ]



    comparison = []



    for metric in metrics:


        company_value = company_row.get(
            metric,
            None
        )


        average_value = df[metric].mean()



        comparison.append(

            {
                "metric": metric,

                "company_value": company_value,

                "n100_average": average_value

            }

        )



    result = pd.DataFrame(
        comparison
    )



    os.makedirs(
        "output",
        exist_ok=True
    )



    result.to_csv(
        OUTPUT_PATH,
        index=False
    )



    print(
        "\nPeer Comparison:",
        company_row["company_name"]
    )


    print(
        "\n"
    )


    print(result)



    print(
        "\nSaved:",
        OUTPUT_PATH
    )





if __name__ == "__main__":


    company = input(
        "Enter company name: "
    )


    peer_compare(
        company
    )