-- Query 1: Top 5 funds by AUM
SELECT amfi_code, scheme_name, aum_crore
FROM fact_performance
ORDER BY aum_crore DESC
LIMIT 5;

-- Query 2: Average NAV per month for each scheme
SELECT 
    f.scheme_name, 
    d.year, 
    d.month_name, 
    ROUND(AVG(n.nav), 4) AS avg_nav
FROM fact_nav n
JOIN dim_fund f ON n.amfi_code = f.amfi_code
JOIN dim_date d ON n.date = d.date
GROUP BY f.scheme_name, d.year, d.month
ORDER BY f.scheme_name, d.year, d.month;

-- Query 3: SIP YoY Growth
SELECT 
    t1.month AS current_month,
    t1.sip_inflow_crore AS current_inflow_cr,
    t2.month AS prev_year_month,
    t2.sip_inflow_crore AS prev_inflow_cr,
    ROUND(((t1.sip_inflow_crore - t2.sip_inflow_crore) * 100.0 / t2.sip_inflow_crore), 2) AS yoy_growth_pct
FROM monthly_sip_inflows t1
JOIN monthly_sip_inflows t2 
  ON strftime('%m', t1.month || '-01') = strftime('%m', t2.month || '-01')
  AND CAST(strftime('%Y', t1.month || '-01') AS INTEGER) = CAST(strftime('%Y', t2.month || '-01') AS INTEGER) + 1
ORDER BY current_month;

-- Query 4: Transactions by State
SELECT 
    state, 
    COUNT(*) AS transaction_count, 
    ROUND(SUM(amount_inr), 2) AS total_transaction_amount_inr
FROM fact_transactions
GROUP BY state
ORDER BY total_transaction_amount_inr DESC;

-- Query 5: Funds with expense_ratio < 1%
SELECT amfi_code, scheme_name, expense_ratio_pct
FROM dim_fund
WHERE expense_ratio_pct < 1.0
ORDER BY expense_ratio_pct ASC;

-- Query 6: Total investment amount vs redemption amount by state
SELECT 
    state,
    ROUND(SUM(CASE WHEN transaction_type IN ('SIP', 'Lumpsum') THEN amount_inr ELSE 0 END), 2) AS total_inflow_inr,
    ROUND(SUM(CASE WHEN transaction_type = 'Redemption' THEN amount_inr ELSE 0 END), 2) AS total_outflow_inr,
    ROUND(SUM(CASE WHEN transaction_type IN ('SIP', 'Lumpsum') THEN amount_inr ELSE -amount_inr END), 2) AS net_inflow_inr
FROM fact_transactions
GROUP BY state
ORDER BY net_inflow_inr DESC;

-- Query 7: Sector Weight and Market Value in Portfolio Holdings
SELECT 
    sector, 
    ROUND(SUM(weight_pct) / COUNT(DISTINCT amfi_code), 2) AS avg_weight_per_fund_pct, 
    ROUND(SUM(market_value_cr), 2) AS total_market_value_cr
FROM portfolio_holdings
GROUP BY sector
ORDER BY total_market_value_cr DESC;

-- Query 8: Average Transaction Amount by Gender and Age Group
SELECT 
    gender, 
    age_group, 
    COUNT(*) AS tx_count, 
    ROUND(AVG(amount_inr), 2) AS avg_tx_amount_inr
FROM fact_transactions
GROUP BY gender, age_group
ORDER BY gender, age_group;

-- Query 9: Fund Performance (3-Year Return) vs Expense Ratio Comparison
SELECT 
    f.scheme_name, 
    f.expense_ratio_pct, 
    p.return_3yr_pct, 
    p.sharpe_ratio, 
    p.risk_grade
FROM dim_fund f
JOIN fact_performance p ON f.amfi_code = p.amfi_code
ORDER BY f.expense_ratio_pct DESC;

-- Query 10: Total category-wise net inflows trend
SELECT 
    category, 
    SUM(net_inflow_crore) AS total_net_inflow_crore
FROM category_inflows
GROUP BY category
ORDER BY total_net_inflow_crore DESC;
