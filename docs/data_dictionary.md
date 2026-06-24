# Data Dictionary: Mutual Fund Data Engineering Database

This document lists all the tables, columns, data types, business definitions, and source references in the SQLite database `bluestock_mf.db`.

---

## 1. Dimension Tables

### `dim_fund`
* **Description:** Master directory containing details about individual mutual fund schemes.
* **Source Reference:** Cleaned from `01_fund_master.csv`.
* **Primary Key:** `amfi_code`

| Column Name | SQL Type | Constraint | Business Definition |
| :--- | :--- | :--- | :--- |
| `amfi_code` | INTEGER | PRIMARY KEY | Unique Association of Mutual Funds in India (AMFI) code representing the scheme. |
| `fund_house` | TEXT | NOT NULL | Name of the Asset Management Company (AMC) managing the fund (e.g., SBI Mutual Fund). |
| `scheme_name` | TEXT | NOT NULL | The official name of the mutual fund scheme. |
| `category` | TEXT | - | Asset class category (e.g., Equity, Debt, Hybrid). |
| `sub_category` | TEXT | - | Detailed sub-classification (e.g., Small Cap, Gilt, Liquid). |
| `plan` | TEXT | - | Scheme plan type (e.g., Direct Plan or Regular Plan). |
| `launch_date` | TEXT | - | Launch date of the fund formatted as YYYY-MM-DD. |
| `benchmark` | TEXT | - | Index against which the fund's returns are compared (e.g., NIFTY 50 TRI). |
| `expense_ratio_pct`| REAL | - | Annual fee charged by the fund, expressed as a percentage of AUM. |
| `exit_load_pct` | REAL | - | Penalty fee charged to investors who redeem units early. |
| `min_sip_amount` | REAL | - | Minimum investment amount allowed for Systematic Investment Plan (SIP). |
| `min_lumpsum_amount`| REAL | - | Minimum investment amount allowed for a one-time (lumpsum) purchase. |
| `fund_manager` | TEXT | - | Name of the primary portfolio manager. |
| `risk_category` | TEXT | - | Risk tier classification of the fund (e.g., Moderate, Very High). |
| `sebi_category_code`| TEXT | - | SEBI standardized classification code (e.g., EC01). |

---

### `dim_date`
* **Description:** Time dimension table for analytical queries.
* **Source Reference:** Dynamically generated from unique dates across all loaded tables.
* **Primary Key:** `date`

| Column Name | SQL Type | Constraint | Business Definition |
| :--- | :--- | :--- | :--- |
| `date` | TEXT | PRIMARY KEY | Calendar date in YYYY-MM-DD format. |
| `year` | INTEGER | NOT NULL | Year component (e.g., 2024). |
| `month` | INTEGER | NOT NULL | Numeric month component (1 to 12). |
| `day` | INTEGER | NOT NULL | Calendar day component (1 to 31). |
| `quarter` | INTEGER | NOT NULL | Financial calendar quarter (1 to 4). |
| `day_of_week` | INTEGER | NOT NULL | Day index (0 = Monday, 6 = Sunday). |
| `day_name` | TEXT | NOT NULL | Textual name of the day (e.g., Monday). |
| `month_name` | TEXT | NOT NULL | Full name of the month (e.g., January). |
| `is_weekend` | INTEGER | NOT NULL | Flag indicating weekend (1 = Saturday/Sunday, 0 = Weekday). |

---

## 2. Fact Tables

### `fact_nav`
* **Description:** Daily Net Asset Value (NAV) records of mutual fund schemes.
* **Source Reference:** Cleaned from `02_nav_history.csv` (weekends and holidays are forward-filled).
* **Composite Primary Key:** (`amfi_code`, `date`)

| Column Name | SQL Type | Constraint | Business Definition |
| :--- | :--- | :--- | :--- |
| `amfi_code` | INTEGER | FOREIGN KEY | References `dim_fund(amfi_code)`. |
| `date` | TEXT | FOREIGN KEY | References `dim_date(date)`. |
| `nav` | REAL | NOT NULL | Daily Net Asset Value of the scheme in INR (must be > 0). |

---

### `fact_transactions`
* **Description:** Individual investment and redemption transactions made by retail investors.
* **Source Reference:** Cleaned from `08_investor_transactions.csv`.
* **Primary Key:** `transaction_id` (AUTOINCREMENT)

| Column Name | SQL Type | Constraint | Business Definition |
| :--- | :--- | :--- | :--- |
| `transaction_id` | INTEGER | PRIMARY KEY | Auto-incrementing primary key for each unique transaction. |
| `investor_id` | TEXT | NOT NULL | Anonymised unique identifier of the retail investor. |
| `transaction_date`| TEXT | FOREIGN KEY | References `dim_date(date)`. Format: YYYY-MM-DD. |
| `amfi_code` | INTEGER | FOREIGN KEY | References `dim_fund(amfi_code)`. |
| `transaction_type`| TEXT | NOT NULL | Type of transaction: `SIP`, `Lumpsum`, or `Redemption`. |
| `amount_inr` | REAL | NOT NULL | Transaction value in Indian Rupees (must be > 0). |
| `state` | TEXT | - | Indian state where the investor resides. |
| `city` | TEXT | - | City where the investor resides. |
| `city_tier` | INTEGER | - | Tier classification of the city (e.g., 1, 2, 3). |
| `age_group` | TEXT | - | Age group of the investor (e.g., 18-25, 26-35). |
| `gender` | TEXT | - | Gender of the investor. |
| `annual_income_lakh`| REAL | - | Declared annual income of the investor in Lakhs. |
| `payment_mode` | TEXT | - | Method of transaction payment (e.g., Net Banking, UPI, Cheque). |
| `kyc_status` | TEXT | - | Know Your Customer verification status (e.g., Verified, Pending). |

---

### `fact_performance`
* **Description:** Historical return and risk metrics for each mutual fund scheme.
* **Source Reference:** Cleaned from `07_scheme_performance.csv`.
* **Primary Key:** `amfi_code`

| Column Name | SQL Type | Constraint | Business Definition |
| :--- | :--- | :--- | :--- |
| `amfi_code` | INTEGER | PRIMARY KEY | References `dim_fund(amfi_code)`. |
| `scheme_name` | TEXT | NOT NULL | Scheme name. |
| `fund_house` | TEXT | NOT NULL | Name of the AMC. |
| `category` | TEXT | - | Scheme category. |
| `plan` | TEXT | - | Scheme plan type. |
| `return_1yr_pct` | REAL | - | 1-year annualized return percentage. |
| `return_3yr_pct` | REAL | - | 3-year annualized return percentage. |
| `return_5yr_pct` | REAL | - | 5-year annualized return percentage. |
| `benchmark_3yr_pct`| REAL | - | 3-year annualized return percentage of the fund's index benchmark. |
| `alpha` | REAL | - | Measure of the fund's excess return relative to its benchmark. |
| `beta` | REAL | - | Measure of the fund's volatility relative to its benchmark. |
| `sharpe_ratio` | REAL | - | Risk-adjusted return measure (excess return per unit of volatility). |
| `sortino_ratio` | REAL | - | Risk-adjusted return measure focusing only on downside risk. |
| `std_dev_ann_pct` | REAL | - | Annualised standard deviation of returns (volatility measure). |
| `max_drawdown_pct` | REAL | - | Peak-to-trough decline percentage during the historical period. |
| `aum_crore` | REAL | - | Current assets under management in crore INR. |
| `expense_ratio_pct`| REAL | - | Fund expense ratio in percentage. |
| `morningstar_rating`| INTEGER | - | Morningstar star rating (1 to 5 stars). |
| `risk_grade` | TEXT | - | Risk rating based on volatility. |
| `is_anomaly` | INTEGER | - | Outlier flag: 1 = Return outlier (> 2 std devs from mean), 0 = Normal. |

---

### `fact_aum`
* **Description:** Asset Under Management historical logs grouped by fund house (AMC).
* **Source Reference:** Cleaned from `03_aum_by_fund_house.csv`.
* **Composite Primary Key:** (`date`, `fund_house`)

| Column Name | SQL Type | Constraint | Business Definition |
| :--- | :--- | :--- | :--- |
| `date` | TEXT | FOREIGN KEY | References `dim_date(date)`. Format: YYYY-MM-DD. |
| `fund_house` | TEXT | NOT NULL | Name of the AMC. |
| `aum_lakh_crore` | REAL | - | AMC assets under management in Lakh Crores. |
| `aum_crore` | REAL | - | AMC assets under management in Crores. |
| `num_schemes` | INTEGER | - | Number of active schemes managed by the AMC. |

---

## 3. Supporting Tables

### `portfolio_holdings`
* **Description:** Stock-level equity holdings within each mutual fund portfolio.
* **Source Reference:** Cleaned from `09_portfolio_holdings.csv`.
* **Composite Primary Key:** (`amfi_code`, `stock_symbol`, `portfolio_date`)

| Column Name | SQL Type | Constraint | Business Definition |
| :--- | :--- | :--- | :--- |
| `amfi_code` | INTEGER | FOREIGN KEY | References `dim_fund(amfi_code)`. |
| `stock_symbol` | TEXT | NOT NULL | Ticker/stock symbol of the underlying holding (e.g., RELIANCE). |
| `stock_name` | TEXT | NOT NULL | Full company name of the holding. |
| `sector` | TEXT | - | Business sector category (e.g., Banking, IT, Pharma). |
| `weight_pct` | REAL | - | Percentage allocation of this stock in the fund's total assets. |
| `market_value_cr` | REAL | - | Current market value of the stock holding in crore INR. |
| `current_price_inr`| REAL | - | Current share price of the stock. |
| `portfolio_date` | TEXT | FOREIGN KEY | References `dim_date(date)`. Format: YYYY-MM-DD. |

---

### `benchmark_indices`
* **Description:** Daily historical closing prices for market indices.
* **Source Reference:** Cleaned from `10_benchmark_indices.csv`.
* **Composite Primary Key:** (`date`, `index_name`)

| Column Name | SQL Type | Constraint | Business Definition |
| :--- | :--- | :--- | :--- |
| `date` | TEXT | FOREIGN KEY | References `dim_date(date)`. Format: YYYY-MM-DD. |
| `index_name` | TEXT | NOT NULL | Index name (e.g., NIFTY50, NIFTY_MIDCAP_150). |
| `close_value` | REAL | - | Closing level of the index on that date. |

---

### `monthly_sip_inflows`
* **Description:** Monthly aggregated systematic investment plan inflows for the industry.
* **Source Reference:** Cleaned from `04_monthly_sip_inflows.csv`.
* **Primary Key:** `month`

| Column Name | SQL Type | Constraint | Business Definition |
| :--- | :--- | :--- | :--- |
| `month` | TEXT | PRIMARY KEY | Calendar month in YYYY-MM format. |
| `sip_inflow_crore` | REAL | - | Total SIP investment received during the month in crores. |
| `active_sip_accounts_crore` | REAL | - | Active SIP account count in crores. |
| `new_sip_accounts_lakh` | REAL | - | Count of new SIP accounts opened in lakhs. |
| `sip_aum_lakh_crore` | REAL | - | Aggregate SIP assets under management in Lakh Crores. |
| `yoy_growth_pct` | REAL | - | Year-over-Year growth percentage. |

---

### `category_inflows`
* **Description:** Monthly net inflow amounts categorized by mutual fund classes.
* **Source Reference:** Cleaned from `05_category_inflows.csv`.
* **Composite Primary Key:** (`month`, `category`)

| Column Name | SQL Type | Constraint | Business Definition |
| :--- | :--- | :--- | :--- |
| `month` | TEXT | - | Calendar month in YYYY-MM format. |
| `category` | TEXT | - | Mutual fund category classification (e.g., Large Cap, Mid Cap). |
| `net_inflow_crore` | REAL | - | Net monthly inflow (investments minus redemptions) in crores. |

---

### `industry_folio_count`
* **Description:** Folio counts aggregated at the industry level for equity, debt, hybrid, and other classes.
* **Source Reference:** Cleaned from `06_industry_folio_count.csv`.
* **Primary Key:** `month`

| Column Name | SQL Type | Constraint | Business Definition |
| :--- | :--- | :--- | :--- |
| `month` | TEXT | PRIMARY KEY | Calendar month in YYYY-MM format. |
| `total_folios_crore` | REAL | - | Total mutual fund folios (accounts) in crores. |
| `equity_folios_crore`| REAL | - | Equity mutual fund folios in crores. |
| `debt_folios_crore` | REAL | - | Debt mutual fund folios in crores. |
| `hybrid_folios_crore`| REAL | - | Hybrid mutual fund folios in crores. |
| `others_folios_crore`| REAL | - | All other category folios (ETF, FoF, etc.) in crores. |
