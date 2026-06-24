import os
import sqlite3
import pandas as pd

conn = sqlite3.connect("bluestock_mf.db")

with open("sql/schema.sql", "r") as f:
    schema_sql = f.read()

conn.executescript(schema_sql)

processed_dir = "Data/processed"
files_to_tables = {
    "01_fund_master.csv": "dim_fund",
    "02_nav_history.csv": "fact_nav",
    "03_aum_by_fund_house.csv": "fact_aum",
    "04_monthly_sip_inflows.csv": "monthly_sip_inflows",
    "05_category_inflows.csv": "category_inflows",
    "06_industry_folio_count.csv": "industry_folio_count",
    "07_scheme_performance.csv": "fact_performance",
    "08_investor_transactions.csv": "fact_transactions",
    "09_portfolio_holdings.csv": "portfolio_holdings",
    "10_benchmark_indices.csv": "benchmark_indices"
}

loaded_dfs = {}
for filename, table_name in files_to_tables.items():
    df = pd.read_csv(os.path.join(processed_dir, filename))
    loaded_dfs[table_name] = df
    df.to_sql(table_name, conn, if_exists="append", index=False)

unique_dates = set()
if "fact_nav" in loaded_dfs:
    unique_dates.update(loaded_dfs["fact_nav"]["date"].dropna().unique())
if "fact_transactions" in loaded_dfs:
    unique_dates.update(loaded_dfs["fact_transactions"]["transaction_date"].dropna().unique())
if "fact_aum" in loaded_dfs:
    unique_dates.update(loaded_dfs["fact_aum"]["date"].dropna().unique())
if "portfolio_holdings" in loaded_dfs:
    unique_dates.update(loaded_dfs["portfolio_holdings"]["portfolio_date"].dropna().unique())
if "benchmark_indices" in loaded_dfs:
    unique_dates.update(loaded_dfs["benchmark_indices"]["date"].dropna().unique())

dates_series = pd.to_datetime(list(unique_dates))
df_date = pd.DataFrame()
df_date["date"] = dates_series.strftime("%Y-%m-%d")
df_date["year"] = dates_series.year
df_date["month"] = dates_series.month
df_date["day"] = dates_series.day
df_date["quarter"] = dates_series.quarter
df_date["day_of_week"] = dates_series.dayofweek
df_date["day_name"] = dates_series.day_name()
df_date["month_name"] = dates_series.month_name()
df_date["is_weekend"] = df_date["day_of_week"].apply(lambda x: 1 if x >= 5 else 0)

df_date = df_date.drop_duplicates(subset=["date"]).sort_values("date")
df_date.to_sql("dim_date", conn, if_exists="append", index=False)

conn.close()

print("Database loaded successfully!")
