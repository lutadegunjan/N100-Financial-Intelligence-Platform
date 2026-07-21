import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3


# -------------------------
# Page Configuration
# -------------------------

st.set_page_config(
    page_title="N100 Financial Intelligence Platform",
    layout="wide"
)


st.title("📊 N100 Financial Intelligence Platform")
st.write(
    "Financial health analysis and ranking of Nifty 100 companies"
)


# -------------------------
# Load Scorecard
# -------------------------

scorecard = pd.read_csv(
    "output/financial_scorecard.csv"
)


# -------------------------
# KPI Section
# -------------------------

col1, col2, col3 = st.columns(3)


with col1:
    st.metric(
        "Companies Analyzed",
        len(scorecard)
    )


with col2:
    avg_score = round(
        scorecard["financial_score"].mean(),
        2
    )

    st.metric(
        "Average Financial Score",
        avg_score
    )


with col3:
    best = scorecard.iloc[0]["company_name"]

    st.metric(
        "Top Ranked Company",
        best
    )


# -------------------------
# Top Companies
# -------------------------

st.subheader(
    "🏆 Top Financial Performers"
)


top10 = scorecard.sort_values(
    "financial_score",
    ascending=False
).head(10)


st.dataframe(
    top10,
    use_container_width=True
)


# -------------------------
# Charts
# -------------------------

st.subheader(
    "Financial Score Visualization"
)


chart1 = "output/top_financial_score.png"

st.image(
    chart1,
    use_container_width=True
)


st.subheader(
    "Rating Distribution"
)


chart2 = "output/rating_distribution.png"


st.image(
    chart2,
    use_container_width=True
)


# -------------------------
# Rating Analysis
# -------------------------

st.subheader(
    "Company Rating Summary"
)


rating_summary = (
    scorecard["rating"]
    .value_counts()
    .reset_index()
)

rating_summary.columns = [
    "Rating",
    "Companies"
]


st.bar_chart(
    rating_summary.set_index("Rating")
)