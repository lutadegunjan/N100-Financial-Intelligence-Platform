import pandas as pd
import os


SCREENER_FILE = "output/screener_results.csv"
PEER_FILE = "output/peer_comparison.csv"

OUTPUT_FILE = "output/financial_screening_report.txt"



def load_files():

    screener = pd.read_csv(
        SCREENER_FILE
    )


    peer = None

    if os.path.exists(PEER_FILE):

        peer = pd.read_csv(
            PEER_FILE
        )


    return screener, peer




def generate_report():

    screener, peer = load_files()


    os.makedirs(
        "output",
        exist_ok=True
    )


    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:



        file.write(
            "N100 FINANCIAL INTELLIGENCE PLATFORM\n"
        )

        file.write(
            "Financial Screening Report\n"
        )

        file.write(
            "=" * 50 + "\n\n"
        )



        # Top companies

        file.write(
            "TOP RANKED COMPANIES\n"
        )

        file.write(
            "-" * 30 + "\n"
        )


        top = screener.head(10)


        for index, row in top.iterrows():

            file.write(

                f"{index + 1}. "
                f"{row['company_name']} "
                f"- Score: {row['score']}\n"

            )



        file.write(
            "\n\n"
        )



        # Peer comparison

        if peer is not None:


            file.write(
                "PEER COMPARISON SUMMARY\n"
            )


            file.write(
                "-" * 30 + "\n"
            )


            for _, row in peer.iterrows():


                company_value = row["company_value"]

                average = row["n100_average"]



                if pd.isna(company_value):

                    company_value = "NA"


                if pd.isna(average):

                    average = "NA"



                file.write(

                    f"{row['metric']}: "
                    f"Company={company_value}, "
                    f"N100 Average={average}\n"

                )


        else:

            file.write(
                "No peer comparison available.\n"
            )



    print(
        "Report generated:"
    )

    print(
        OUTPUT_FILE
    )




if __name__ == "__main__":

    generate_report()