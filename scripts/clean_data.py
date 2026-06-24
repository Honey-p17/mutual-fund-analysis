import os
import pandas as pd

raw_dir = "Data/raw"
processed_dir = "Data/processed"

if not os.path.exists(processed_dir):
    os.makedirs(processed_dir)

def load_csv(filename):
    return pd.read_csv(os.path.join(raw_dir, filename))

def save_csv(df, filename):
    df.to_csv(os.path.join(processed_dir, filename), index=False)

df_fund = load_csv("01_fund_master.csv")
for col in df_fund.select_dtypes(include=['object']).columns:
    df_fund[col] = df_fund[col].astype(str).str.strip()
df_fund['launch_date'] = pd.to_datetime(df_fund['launch_date']).dt.strftime('%Y-%m-%d')
df_fund = df_fund.drop_duplicates()
save_csv(df_fund, "01_fund_master.csv")

df_nav = load_csv("02_nav_history.csv")
df_nav['date'] = pd.to_datetime(df_nav['date'])
df_nav = df_nav.sort_values(by=['amfi_code', 'date'])
df_nav = df_nav.drop_duplicates(subset=['amfi_code', 'date'])
df_nav = df_nav[df_nav['nav'] > 0]

nav_list = []
for amfi, group in df_nav.groupby('amfi_code'):
    group = group.set_index('date')
    date_range = pd.date_range(start=group.index.min(), end=group.index.max(), freq='D')
    group_filled = group.reindex(date_range)
    group_filled['amfi_code'] = amfi
    group_filled['nav'] = group_filled['nav'].ffill()
    group_filled = group_filled.reset_index().rename(columns={'index': 'date'})
    nav_list.append(group_filled)

df_nav_clean = pd.concat(nav_list, ignore_index=True)
df_nav_clean['date'] = df_nav_clean['date'].dt.strftime('%Y-%m-%d')
save_csv(df_nav_clean, "02_nav_history.csv")

df_aum = load_csv("03_aum_by_fund_house.csv")
for col in df_aum.select_dtypes(include=['object']).columns:
    df_aum[col] = df_aum[col].astype(str).str.strip()
df_aum['date'] = pd.to_datetime(df_aum['date']).dt.strftime('%Y-%m-%d')
df_aum = df_aum.drop_duplicates()
save_csv(df_aum, "03_aum_by_fund_house.csv")

df_sip = load_csv("04_monthly_sip_inflows.csv")
df_sip['month'] = pd.to_datetime(df_sip['month'], format='%Y-%m').dt.strftime('%Y-%m')
df_sip = df_sip.drop_duplicates()
save_csv(df_sip, "04_monthly_sip_inflows.csv")

df_cat = load_csv("05_category_inflows.csv")
for col in df_cat.select_dtypes(include=['object']).columns:
    df_cat[col] = df_cat[col].astype(str).str.strip()
df_cat['month'] = pd.to_datetime(df_cat['month'], format='%Y-%m').dt.strftime('%Y-%m')
df_cat = df_cat.drop_duplicates()
save_csv(df_cat, "05_category_inflows.csv")

df_folios = load_csv("06_industry_folio_count.csv")
df_folios['month'] = pd.to_datetime(df_folios['month'], format='%Y-%m').dt.strftime('%Y-%m')
df_folios = df_folios.drop_duplicates()
save_csv(df_folios, "06_industry_folio_count.csv")

df_perf = load_csv("07_scheme_performance.csv")
for col in df_perf.select_dtypes(include=['object']).columns:
    df_perf[col] = df_perf[col].astype(str).str.strip()
for col in ['return_1yr_pct', 'return_3yr_pct', 'return_5yr_pct', 'benchmark_3yr_pct']:
    df_perf[col] = pd.to_numeric(df_perf[col], errors='coerce').fillna(0.0)

df_perf['is_anomaly'] = 0
mean_3yr = df_perf['return_3yr_pct'].mean()
std_3yr = df_perf['return_3yr_pct'].std()
anomalies = df_perf[((df_perf['return_3yr_pct'] - mean_3yr).abs() / std_3yr) > 2.0]
df_perf.loc[anomalies.index, 'is_anomaly'] = 1
df_perf = df_perf.drop_duplicates()
save_csv(df_perf, "07_scheme_performance.csv")

df_tx = load_csv("08_investor_transactions.csv")
for col in df_tx.select_dtypes(include=['object']).columns:
    df_tx[col] = df_tx[col].astype(str).str.strip()
df_tx['transaction_type'] = df_tx['transaction_type'].replace({
    'sip': 'SIP', 'Sip': 'SIP',
    'lumpsum': 'Lumpsum', 'Lump Sum': 'Lumpsum', 'lump_sum': 'Lumpsum',
    'redemption': 'Redemption', 'Redeem': 'Redemption'
})
df_tx = df_tx[df_tx['amount_inr'] > 0]
df_tx['transaction_date'] = pd.to_datetime(df_tx['transaction_date']).dt.strftime('%Y-%m-%d')
df_tx['kyc_status'] = df_tx['kyc_status'].replace({
    'verified': 'Verified', 'VERIFIED': 'Verified',
    'pending': 'Pending', 'PENDING': 'Pending'
})
df_tx = df_tx.drop_duplicates()
save_csv(df_tx, "08_investor_transactions.csv")

df_port = load_csv("09_portfolio_holdings.csv")
for col in df_port.select_dtypes(include=['object']).columns:
    df_port[col] = df_port[col].astype(str).str.strip()
df_port['portfolio_date'] = pd.to_datetime(df_port['portfolio_date']).dt.strftime('%Y-%m-%d')
df_port = df_port.drop_duplicates()
save_csv(df_port, "09_portfolio_holdings.csv")

df_bench = load_csv("10_benchmark_indices.csv")
for col in df_bench.select_dtypes(include=['object']).columns:
    df_bench[col] = df_bench[col].astype(str).str.strip()
df_bench['date'] = pd.to_datetime(df_bench['date']).dt.strftime('%Y-%m-%d')
df_bench = df_bench.drop_duplicates()
save_csv(df_bench, "10_benchmark_indices.csv")

print("Successfully cleaned all 10 raw CSV files!")
