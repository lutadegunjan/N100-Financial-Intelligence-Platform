import os
import pandas as pd

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

DATASET_DIR = os.path.join(BASE_DIR, "Data Sets")
SUPPORTING_DIR = os.path.join(BASE_DIR, "Supporting datasets")

FILES = {
    "companies": os.path.join(DATASET_DIR, "companies.xlsx"),
    "profitandloss": os.path.join(DATASET_DIR, "profitandloss.xlsx"),
    "balancesheet": os.path.join(DATASET_DIR, "balancesheet.xlsx"),
    "cashflow": os.path.join(DATASET_DIR, "cashflow.xlsx"),
    "analysis": os.path.join(DATASET_DIR, "analysis.xlsx"),
    "documents": os.path.join(DATASET_DIR, "documents.xlsx"),
    "prosandcons": os.path.join(DATASET_DIR, "prosandcons.xlsx"),

    "financial_ratios": os.path.join(SUPPORTING_DIR, "financial_ratios.xlsx"),
    "market_cap": os.path.join(SUPPORTING_DIR, "market_cap.xlsx"),
    "peer_groups": os.path.join(SUPPORTING_DIR, "peer_groups.xlsx"),
    "sectors": os.path.join(SUPPORTING_DIR, "sectors.xlsx"),
    "stock_prices": os.path.join(SUPPORTING_DIR, "stock_prices.xlsx"),
}


def load_excel_files() -> dict[str, pd.DataFrame]:
    """
    Load all Excel datasets into pandas DataFrames.

    Returns:
        Dictionary containing dataset names as keys
        and pandas DataFrames as values.
    """

    datasets = {}

    for name, path in FILES.items():

        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Dataset missing: {path}"
            )

        try:
            # Core datasets have an extra title row
            if name in [
                "companies",
                "profitandloss",
                "balancesheet",
                "cashflow",
                "analysis",
                "documents",
                "prosandcons"
            ]:
                df = pd.read_excel(path, header=1)

            # Supporting datasets have headers in the first row
            else:
                df = pd.read_excel(path)

            datasets[name] = df

        except Exception as e:
            raise RuntimeError(
                f"Failed loading {name}: {e}"
            )

    return datasets


if __name__ == "__main__":

    data = load_excel_files()

    print("Loaded datasets:\n")

    for name, df in data.items():
        print(f"{name:<20} {df.shape}")