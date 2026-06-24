DROP TABLE IF EXISTS fact_nav;
DROP TABLE IF EXISTS fact_transactions;
DROP TABLE IF EXISTS fact_performance;
DROP TABLE IF EXISTS fact_aum;
DROP TABLE IF EXISTS portfolio_holdings;
DROP TABLE IF EXISTS benchmark_indices;
DROP TABLE IF EXISTS monthly_sip_inflows;
DROP TABLE IF EXISTS category_inflows;
DROP TABLE IF EXISTS industry_folio_count;
DROP TABLE IF EXISTS dim_fund;
DROP TABLE IF EXISTS dim_date;

CREATE TABLE dim_fund (
    amfi_code INTEGER PRIMARY KEY,
    fund_house TEXT NOT NULL,
    scheme_name TEXT NOT NULL,
    category TEXT,
    sub_category TEXT,
    plan TEXT,
    launch_date TEXT,
    benchmark TEXT,
    expense_ratio_pct REAL,
    exit_load_pct REAL,
    min_sip_amount REAL,
    min_lumpsum_amount REAL,
    fund_manager TEXT,
    risk_category TEXT,
    sebi_category_code TEXT
);

CREATE TABLE dim_date (
    date TEXT PRIMARY KEY,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    day INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    day_of_week INTEGER NOT NULL,
    day_name TEXT NOT NULL,
    month_name TEXT NOT NULL,
    is_weekend INTEGER NOT NULL
);

CREATE TABLE fact_nav (
    amfi_code INTEGER,
    date TEXT,
    nav REAL NOT NULL,
    PRIMARY KEY (amfi_code, date),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY (date) REFERENCES dim_date(date)
);

CREATE TABLE fact_transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id TEXT NOT NULL,
    transaction_date TEXT NOT NULL,
    amfi_code INTEGER NOT NULL,
    transaction_type TEXT NOT NULL,
    amount_inr REAL NOT NULL,
    state TEXT,
    city TEXT,
    city_tier INTEGER,
    age_group TEXT,
    gender TEXT,
    annual_income_lakh REAL,
    payment_mode TEXT,
    kyc_status TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY (transaction_date) REFERENCES dim_date(date)
);

CREATE TABLE fact_performance (
    amfi_code INTEGER PRIMARY KEY,
    scheme_name TEXT NOT NULL,
    fund_house TEXT NOT NULL,
    category TEXT,
    plan TEXT,
    return_1yr_pct REAL,
    return_3yr_pct REAL,
    return_5yr_pct REAL,
    benchmark_3yr_pct REAL,
    alpha REAL,
    beta REAL,
    sharpe_ratio REAL,
    sortino_ratio REAL,
    std_dev_ann_pct REAL,
    max_drawdown_pct REAL,
    aum_crore REAL,
    expense_ratio_pct REAL,
    morningstar_rating INTEGER,
    risk_grade TEXT,
    is_anomaly INTEGER,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE TABLE fact_aum (
    date TEXT NOT NULL,
    fund_house TEXT NOT NULL,
    aum_lakh_crore REAL,
    aum_crore REAL,
    num_schemes INTEGER,
    PRIMARY KEY (date, fund_house),
    FOREIGN KEY (date) REFERENCES dim_date(date)
);

CREATE TABLE portfolio_holdings (
    amfi_code INTEGER,
    stock_symbol TEXT,
    stock_name TEXT NOT NULL,
    sector TEXT,
    weight_pct REAL,
    market_value_cr REAL,
    current_price_inr REAL,
    portfolio_date TEXT,
    PRIMARY KEY (amfi_code, stock_symbol, portfolio_date),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY (portfolio_date) REFERENCES dim_date(date)
);

CREATE TABLE benchmark_indices (
    date TEXT,
    index_name TEXT,
    close_value REAL,
    PRIMARY KEY (date, index_name),
    FOREIGN KEY (date) REFERENCES dim_date(date)
);

CREATE TABLE monthly_sip_inflows (
    month TEXT PRIMARY KEY,
    sip_inflow_crore REAL,
    active_sip_accounts_crore REAL,
    new_sip_accounts_lakh REAL,
    sip_aum_lakh_crore REAL,
    yoy_growth_pct REAL
);

CREATE TABLE category_inflows (
    month TEXT,
    category TEXT,
    net_inflow_crore REAL,
    PRIMARY KEY (month, category)
);

CREATE TABLE industry_folio_count (
    month TEXT PRIMARY KEY,
    total_folios_crore REAL,
    equity_folios_crore REAL,
    debt_folios_crore REAL,
    hybrid_folios_crore REAL,
    others_folios_crore REAL
);
