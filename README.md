# 📈 N100 Financial Intelligence Platform

An end-to-end Financial Analytics Platform built using Python and SQL to analyze Nifty 100 companies through automated ETL pipelines, financial ratio analysis, stock screening, peer comparison, and visualization.

---

# Project Overview

This project automates the complete financial analysis workflow for Nifty 100 companies.

It includes:

- ETL Pipeline
- SQLite Database
- Data Validation
- Financial Ratio Engine
- Financial Scoring
- Stock Screening
- Peer Comparison
- Radar Charts
- Automated Reports

---

# Tech Stack

### Programming
- Python
- SQL

### Libraries
- Pandas
- NumPy
- Matplotlib
- OpenPyXL
- PyYAML

### Database
- SQLite

---

# System Architecture

![Architecture](assets/screenshots/architecture.png)

---

# Features

## ETL Pipeline

- Data Loading
- Cleaning
- Normalization
- Database Population

---

## Financial Ratio Engine

Calculates:

- ROE
- ROCE
- ROA
- Net Profit Margin
- Revenue CAGR
- PAT CAGR

---

## Financial Scoring

Ranks companies using multiple financial metrics.

### Sample Output

![Financial Score](assets/screenshots/top_score.png)

---

## Stock Screening

Supports custom screening using:

- ROE
- Debt Equity
- CAGR
- Profitability
- Valuation

### Sample Output

![Screening](assets/screenshots/screener.png)

---

## Peer Comparison

Compares a company against industry peers.

### Sample Output

![Peer Comparison](assets/screenshots/peer.png)

---

## Radar Charts

Visual comparison of company financial strength.

### Example

![Radar Chart](assets/screenshots/radar.png)

---

# Generated Outputs

The project automatically generates:

- Financial Scorecards
- Screening Reports
- Peer Comparison Reports
- Radar Charts
- Excel Reports
- Data Quality Reports

---

# Folder Structure

```
src/
analytics/
etl/
screener/
reports/
output/
db/
tests/
```

---

# How to Run

Clone repository

```bash
git clone https://github.com/lutadegunjan/N100-Financial-Intelligence-Platform.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run Validation

```bash
python src/run_validation.py
```

Run Financial Scoring

```bash
python src/financial_score.py
```

Run Stock Screener

```bash
python src/screener/screens.py
```

Generate Peer Comparison

```bash
python src/analytics/peer.py
```

Generate Radar Charts

```bash
python src/analytics/radar_chart.py
```

---

# Skills Demonstrated

- Python
- SQL
- ETL Development
- Data Engineering
- Financial Analytics
- Data Validation
- Data Visualization
- Business Intelligence
- Reporting Automation

---

# Author

**Gunjan Lutade**

GitHub:
https://github.com/lutadegunjan

LinkedIn:
https://www.linkedin.com/in/gunjan-lutade-67029b22a/