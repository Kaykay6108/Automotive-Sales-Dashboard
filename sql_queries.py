import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect('C:/Portfolio/automotive.db')

# ── Query 1: Revenue by Make ─────────────────────────────────
q1 = """
SELECT
    make,
    COUNT(*)                          AS units_sold,
    ROUND(SUM(sellingprice), 0)       AS total_revenue,
    ROUND(AVG(sellingprice), 0)       AS avg_price,
    ROUND(AVG(price_vs_mmr_pct), 2)   AS avg_discount_pct
FROM sales
WHERE make != 'Nan'
GROUP BY make
ORDER BY total_revenue DESC
LIMIT 20
"""
df_q1 = pd.read_sql_query(q1, conn)
print("=== Query 1: Top 20 Makes by Revenue ===")
print(df_q1.to_string())
print()

# ── Query 2: Monthly Sales Trend ─────────────────────────────
q2 = """
SELECT
    sale_year,
    sale_month,
    CASE sale_month
        WHEN 1  THEN 'Jan' WHEN 2  THEN 'Feb'
        WHEN 3  THEN 'Mar' WHEN 4  THEN 'Apr'
        WHEN 5  THEN 'May' WHEN 6  THEN 'Jun'
        WHEN 7  THEN 'Jul' WHEN 8  THEN 'Aug'
        WHEN 9  THEN 'Sep' WHEN 10 THEN 'Oct'
        WHEN 11 THEN 'Nov' WHEN 12 THEN 'Dec'
    END AS sale_month_name,
    COUNT(*)                     AS units_sold,
    ROUND(SUM(sellingprice), 0)  AS total_revenue,
    ROUND(AVG(sellingprice), 0)  AS avg_price
FROM sales
WHERE sale_year BETWEEN 2014 AND 2015
GROUP BY sale_year, sale_month
ORDER BY sale_year, sale_month
"""
df_q2 = pd.read_sql_query(q2, conn)
print("=== Query 2: Monthly Sales Trend ===")
print(df_q2.to_string())
print()

# ── Query 3: Performance by State ────────────────────────────
q3 = """
SELECT
    state,
    COUNT(*)                          AS units_sold,
    ROUND(SUM(sellingprice), 0)       AS total_revenue,
    ROUND(AVG(sellingprice), 0)       AS avg_price,
    ROUND(AVG(odometer), 0)           AS avg_mileage
FROM sales
WHERE state != 'Nan'
GROUP BY state
ORDER BY total_revenue DESC
LIMIT 15
"""
df_q3 = pd.read_sql_query(q3, conn)
print("=== Query 3: Top 15 States by Revenue ===")
print(df_q3.to_string())
print()

# ── Query 4: Price vs MMR by Body Type ───────────────────────
q4 = """
SELECT
    body,
    COUNT(*)                          AS units_sold,
    ROUND(AVG(sellingprice), 0)       AS avg_sell_price,
    ROUND(AVG(mmr), 0)                AS avg_market_price,
    ROUND(AVG(price_vs_mmr_pct), 2)   AS avg_price_vs_market_pct,
    CASE
        WHEN AVG(price_vs_mmr_pct) > 0 THEN 'Above Market'
        WHEN AVG(price_vs_mmr_pct) < 0 THEN 'Below Market'
        ELSE 'At Market'
    END AS pricing_position
FROM sales
WHERE body != 'Nan'
GROUP BY body
HAVING COUNT(*) > 100
ORDER BY units_sold DESC
"""
df_q4 = pd.read_sql_query(q4, conn)
print("=== Query 4: Price vs Market by Body Type ===")
print(df_q4.to_string())
print()

# ── Query 5: Year-over-Year Growth ───────────────────────────
q5 = """
SELECT
    sale_year,
    COUNT(*)                     AS units_sold,
    ROUND(SUM(sellingprice), 0)  AS total_revenue,
    ROUND(AVG(sellingprice), 0)  AS avg_price
FROM sales
WHERE sale_year IS NOT NULL
GROUP BY sale_year
ORDER BY sale_year
"""
df_q5 = pd.read_sql_query(q5, conn)
df_q5['revenue_yoy_pct'] = df_q5['total_revenue'].pct_change().mul(100).round(2)
df_q5['units_yoy_pct']   = df_q5['units_sold'].pct_change().mul(100).round(2)
print("=== Query 5: Year-over-Year Growth ===")
print(df_q5.to_string())
print()

# ── Export all results to Excel (one file, multiple sheets) ──
with pd.ExcelWriter('C:/Portfolio/data/sql_results.xlsx', engine='openpyxl') as writer:
    df_q1.to_excel(writer, sheet_name='Revenue_by_Make',  index=False)
    df_q2.to_excel(writer, sheet_name='Monthly_Trend',    index=False)
    df_q3.to_excel(writer, sheet_name='Revenue_by_State', index=False)
    df_q4.to_excel(writer, sheet_name='Price_vs_Market',  index=False)
    df_q5.to_excel(writer, sheet_name='YoY_Growth',       index=False)

print("=== Done! sql_results.xlsx exported ===")
conn.close()
