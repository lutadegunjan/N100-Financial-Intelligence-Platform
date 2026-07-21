import os
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3


BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(OUTPUT_DIR, exist_ok=True)


# -----------------------------
# Load Scorecard
# -----------------------------

score_file = os.path.join(
    OUTPUT_DIR,
    "financial_scorecard.csv"
)

df = pd.read_csv(score_file)


# -----------------------------
# Top 10 Financial Score Chart
# -----------------------------

top10 = df.head(10)


plt.figure(figsize=(10,6))

plt.bar(
    top10["company_name"],
    top10["financial_score"]
)

plt.xticks(
    rotation=75,
    ha="right"
)

plt.title(
    "Top 10 Companies by Financial Score"
)

plt.xlabel(
    "Company"
)

plt.ylabel(
    "Financial Score"
)

plt.tight_layout()


plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "top_financial_score.png"
    )
)

plt.close()


# -----------------------------
# Rating Distribution
# -----------------------------

rating_count = df["rating"].value_counts()


plt.figure(figsize=(7,5))


plt.bar(
    rating_count.index,
    rating_count.values
)


plt.title(
    "Company Rating Distribution"
)

plt.xlabel(
    "Rating"
)

plt.ylabel(
    "Number of Companies"
)


plt.tight_layout()


plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "rating_distribution.png"
    )
)


plt.close()


print("Charts Generated Successfully!")
print("Saved in output folder")