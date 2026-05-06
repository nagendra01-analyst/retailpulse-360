# 📊 KPIs Explained — RetailPulse 360

A breakdown of the 15+ executive KPIs computed by the platform, why they matter, and how they are calculated.

## Revenue & Profitability

| KPI | Formula | Why It Matters |
|---|---|---|
| **Total Revenue** | SUM(unit_price × qty × (1 − discount)) | Top-line growth, board-level metric |
| **Total Profit** | Revenue − Cost | Bottom-line, true business health |
| **Gross Margin %** | (Revenue − Cost) / Revenue × 100 | Pricing power & cost efficiency |
| **Total Cost** | SUM(cost × qty) | Tracks COGS against revenue |

## Order Volume

| KPI | Formula | Why It Matters |
|---|---|---|
| **Total Orders** | COUNT(DISTINCT transaction_id) | Demand signal, traffic proxy |
| **Units Sold** | SUM(quantity) | Inventory planning input |
| **AOV (Avg Order Value)** | Revenue / Orders | Basket strategy, upsell effectiveness |
| **Median Order Value** | PERCENTILE(0.5, order_value) | Distribution insight, robust to outliers |

## Customer Health

| KPI | Formula | Why It Matters |
|---|---|---|
| **Unique Customers** | COUNT(DISTINCT customer_id) | Audience reach |
| **Repeat Customer Rate** | % of customers with > 1 order | Retention quality |
| **Avg Orders per Customer** | Orders / Customers | Loyalty / engagement |
| **CLTV (Customer Lifetime Value)** | AVG(SUM(revenue) per customer) | Long-term value driver |
| **Churn Rate** | % with last purchase > 90 days | Retention risk metric |

## Channel & Promotion

| KPI | Formula | Why It Matters |
|---|---|---|
| **Online Revenue Share %** | Online revenue / Total revenue × 100 | Channel mix, digital maturity |
| **Avg Discount %** | AVG(discount) × 100 | Promo intensity |
| **Discounted Order Share %** | % of orders with discount > 0 | Reliance on discounting |

## Inventory

| KPI | Formula | Why It Matters |
|---|---|---|
| **Stockout Rate** | % SKUs with stock_qty = 0 | Lost sales risk |
| **Inventory Turnover** | COGS / Avg Inventory | Capital efficiency |

## Forecasting

| KPI | Formula | Why It Matters |
|---|---|---|
| **MAPE** | mean(|y − ŷ| / y) × 100 | Forecast accuracy benchmark |
| **90-Day Projected Revenue** | SUM(forecast.yhat[-90:]) | Forward planning input |

## How to Use

1. **Daily** — watch Revenue, Orders, AOV for anomalies
2. **Weekly** — review Repeat Rate, Channel Mix, Discount Share
3. **Monthly** — review CLTV, Churn, Forecast vs Actual, Cohort Retention
4. **Quarterly** — strategic review of category profitability + region performance
