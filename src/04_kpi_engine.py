"""
RetailPulse 360 - KPI Engine
------------------------------
Computes 15+ executive KPIs from the cleaned fact table
and exports them to data/processed/kpis.csv for use
in dashboards and reports.
"""
import pandas as pd

fact = pd.read_parquet("data/processed/fact_sales.parquet")

order_revenue = fact.groupby("transaction_id")["revenue"].sum()

kpis = {
    # ----- Revenue / Profitability -----
    "Total Revenue":          fact["revenue"].sum(),
    "Total Profit":           fact["profit"].sum(),
    "Gross Margin %":         fact["profit"].sum() / fact["revenue"].sum() * 100,
    "Total Cost":             fact["cost"].sum(),

    # ----- Volume -----
    "Total Orders":           fact["transaction_id"].nunique(),
    "Units Sold":             int(fact["quantity"].sum()),
    "Avg Order Value (AOV)":  order_revenue.mean(),
    "Median Order Value":     order_revenue.median(),

    # ----- Customer -----
    "Unique Customers":       fact["customer_id"].nunique(),
    "Repeat Customer Rate %": (fact.groupby("customer_id").size() > 1).mean() * 100,
    "Avg Orders per Customer": fact.groupby("customer_id")["transaction_id"].nunique().mean(),
    "Avg CLTV":               fact.groupby("customer_id")["revenue"].sum().mean(),

    # ----- Product / Channel -----
    "Top Category (Revenue)": fact.groupby("category")["revenue"].sum().idxmax(),
    "Top Region (Revenue)":   fact.groupby("region")["revenue"].sum().idxmax(),
    "Online Revenue Share %": (
        fact.loc[fact["channel"] == "Online", "revenue"].sum()
        / fact["revenue"].sum() * 100
    ),

    # ----- Discount / Promotion -----
    "Avg Discount %":         fact["discount"].mean() * 100,
    "Discounted Order Share %": (fact["discount"] > 0).mean() * 100,
}

series = pd.Series(kpis, name="value")
series.to_csv("data/processed/kpis.csv")

print("=" * 50)
print("  RETAILPULSE 360 - EXECUTIVE KPIs")
print("=" * 50)
for k, v in kpis.items():
    if isinstance(v, float):
        print(f"  {k:30s} : {v:>15,.2f}")
    else:
        print(f"  {k:30s} : {v!s:>15}")
print("=" * 50)
