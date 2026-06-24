import os
import sqlite3
import pandas as pd

conn = sqlite3.connect("bluestock_mf.db")
cursor = conn.cursor()

tables_to_csv = {
    "dim_fund": "01_fund_master.csv",
    "fact_nav": "02_nav_history.csv",
    "fact_aum": "03_aum_by_fund_house.csv",
    "monthly_sip_inflows": "04_monthly_sip_inflows.csv",
    "category_inflows": "05_category_inflows.csv",
    "industry_folio_count": "06_industry_folio_count.csv",
    "fact_performance": "07_scheme_performance.csv",
    "fact_transactions": "08_investor_transactions.csv",
    "portfolio_holdings": "09_portfolio_holdings.csv",
    "benchmark_indices": "10_benchmark_indices.csv"
}

all_matched = True
for table, csv in tables_to_csv.items():
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    db_rows = cursor.fetchone()[0]
    
    df = pd.read_csv(os.path.join("Data/processed", csv))
    csv_rows = len(df)
    
    status = "Match" if db_rows == csv_rows else "Mismatch"
    if status == "Mismatch":
        all_matched = False
    print(f"{table}: CSV={csv_rows}, DB={db_rows} -> {status}")

cursor.execute("SELECT COUNT(*) FROM dim_date")
print(f"dim_date: DB={cursor.fetchone()[0]}")
conn.close()

if all_matched:
    print("All counts match perfectly!")
else:
    print("Warning: Mismatch found!")
