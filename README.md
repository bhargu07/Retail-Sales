# Retail Sales & Customer Analytics Pipeline

An end-to-end analytics project on the Superstore retail dataset — from raw CSV to a normalized SQL database, statistical analysis, and an interactive Power BI dashboard.

## Project Overview

This project simulates a real analyst workflow: data doesn't arrive clean in one file — it needs to be modeled, stored, statistically validated, and then visualized for business stakeholders. This pipeline covers all three stages using **SQL, Python, Excel-style statistics, and Power BI**.

**Business question:** What drives profitability in this retail business, and which customers should the business prioritize retaining?

## Tech Stack

| Stage | Tools |
|---|---|
| Data storage & modeling | MySQL |
| Data loading / ETL | Python (pandas, SQLAlchemy) |
| Statistical analysis | Python (pandas, SciPy) |
| Dashboard & visualization | Power BI (DAX, star schema, RFM segmentation) |

## Dataset

[Sample Superstore dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final) — 9,994 retail order line items across 793 customers and 1,862 products (2014–2017).

## Stage 1: Database Design (SQL)

Raw CSV data was split into a **normalized star schema**:

- **`customers`** (793 rows) — customer_id, name, segment
- **`products`** (1,862 rows) — product_id, name, category, sub_category
- **`orders`** (9,994 rows) — fact table with order details, shipping location, sales, discount, profit — linked to customers and products via foreign keys

A reusable **`sales_master` view** joins all three tables for simplified querying and reporting.

**Key SQL techniques used:**
- Joins across normalized tables
- Window functions — `SUM() OVER()` for running totals, `RANK() OVER()` for top-product ranking by category
- CTEs — month-over-month sales growth (`LAG()`), customer cohort analysis (first-purchase-month grouping)

*(See `analysis_queries.sql` for the full query set.)*

## Stage 2: Statistical Analysis (Python)

Descriptive statistics and hypothesis testing were used to validate business assumptions rather than just visualize them.

**Key findings:**
- **Sales and Profit are right-skewed** — mean sales (₹230) is much higher than median (₹54), driven by a small number of large orders.
- **Discount vs. Profit correlation: -0.22** — a weak-to-moderate negative relationship; discounting hurts profit, but isn't the only driver.
- **Hypothesis test (independent t-test):** Orders with ≥30% discount average **-₹97 profit** (a loss), while orders with <30% discount average **+₹49 profit**. This difference is statistically significant (**p < 0.001**), confirming heavy discounting is a genuine driver of unprofitability, not random variation.

*(See `stats_analysis.py` for the full script.)*

## Stage 3: Power BI Dashboard

An interactive dashboard built on the same normalized SQL tables (live connection, star schema model), featuring:

- **KPI cards** — Total Sales, Total Profit, Profit Margin %, Total Orders
- **Sales by Region & Category** — bar charts
- **Monthly Sales Trend** — line chart showing seasonality
- **Slicers** — Region, Category, Year (fully interactive cross-filtering)
- **RFM Customer Segmentation** — a DAX-driven donut chart classifying all 793 customers into Champion / Loyal Customer / Potential Loyalist / At Risk / Lost, based on Recency and Frequency of orders

**RFM segmentation logic (DAX):**
```dax
Customer Segment = 
SWITCH(
    TRUE(),
    [Recency Days] <= 90 && [Total Orders] >= 5, "Champion",
    [Recency Days] <= 180 && [Total Orders] >= 3, "Loyal Customer",
    [Recency Days] <= 365 && [Total Orders] < 3, "Potential Loyalist",
    [Recency Days] > 365 && [Total Orders] >= 3, "At Risk",
    [Recency Days] > 365 && [Total Orders] < 3, "Lost",
    "Needs Review"
)
```

**Result:** 45% of customers are Champions driving repeat revenue, while 28% are Lost — highlighting a clear win-back opportunity for the business.

## Key Business Insight

> Champions make up 45% of customers and drive the majority of repeat revenue, while 28% are Lost — indicating a strong win-back opportunity. Orders discounted 30%+ lose money on average, while lower-discount orders remain profitable, a statistically significant pattern (p < 0.001). **Recommendation:** cap discounts below 30% on non-clearance items, and launch a targeted win-back campaign for the "Lost" customer segment.

## Repository Structure

```
├── build_database.py       # Python ETL: CSV -> normalized MySQL tables
├── export_data.py          # Exports sales_master view to CSV
├── stats_analysis.py       # Descriptive stats, correlation, t-test
├── analysis_queries.sql    # Joins, window functions, CTEs
├── Flagship_Retail_Analytics.pbix   # Power BI dashboard file
└── README.md
```

## How to Run This Project

1. Import `Sample - Superstore.csv` and run `build_database.py` to build the MySQL database
2. Run `export_data.py` to export the joined dataset
3. Run `stats_analysis.py` for the statistical analysis
4. Open `Flagship_Retail_Analytics.pbix` in Power BI Desktop (update the MySQL connection credentials under Transform Data → Data Source Settings)
