# Automotive-Sales-DashboardAutomotive Sales Dashboard
SQL + Power BI | U.S. Used Vehicle Market Analysis
An end-to-end data analytics project analyzing 490,000+ U.S. used vehicle sales records. Built with Python for data cleaning and SQL-based analysis, visualized in a 4-page Power BI dashboard. (Supported with Claude Ai)
---
Dashboard Pages
1. General Overview
KPI cards (Total Revenue, Units Sold, Avg Selling Price, Avg Discount) with top 20 brands by revenue and monthly sales trend.
![General Overview](screenshots/overview.png)
2. Regional Analysis
Revenue breakdown by U.S. state with interactive map, bar chart, and detailed state performance table with avg price and mileage.
![Regional Analysis](screenshots/regional.png)
3. Price Analysis
Sell price vs. MMR market reference price by vehicle body type, with pricing position classification (Above / Below Market).
![Price Analysis](screenshots/price.png)
4. Executive Summary
High-level snapshot: top 3 brands, top 3 states, and Sedan vs. SUV price comparison alongside overall KPIs.
![Summary](screenshots/summary.png)
---
Project Structure
```
automotive-sales-dashboard/
├── Data.py               # Data cleaning and feature engineering
├── sql_queries.py        # SQL analysis (5 queries via SQLite)
├── data/
│   ├── car_prices.csv        # Raw data (Kaggle)
│   ├── car_prices_clean.csv  # Cleaned dataset
│   └── sql_results.xlsx      # Query outputs (Power BI source)
└── screenshots/
    ├── overview.png
    ├── regional.png
    ├── price.png
    └── summary.png
```
---
Tools & Methods
Layer	Tools
Data Cleaning	Python, Pandas
Analysis	SQL (SQLite), Python
Visualization	Power BI
Version Control	Git, GitHub
SQL techniques used: GROUP BY, ORDER BY, CASE WHEN, HAVING, window functions (YoY via Pandas), subqueries
---
Key Findings
Ford leads total revenue at ~$1.1B, nearly 2x Chevrolet in second place
Florida and California together account for over 30% of total market revenue
SUVs command a ~40% price premium over Sedans on average
Most vehicle body types sell below MMR market reference price, suggesting a buyer's market in the used car segment
---
Data Source
Vehicle Sales Data – Kaggle
---
Acknowledgements
Data cleaning and SQL query development assisted with Claude (Anthropic).
