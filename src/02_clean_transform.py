"""
RetailPulse 360 - Data Cleaning & Transformation
--------------------------------------------------
Reads raw CSVs, performs deduplication, type casting,
feature engineering, and produces a clean fact table
in Parquet format.

Output: data/processed/fact_sales.parquet
"""
import os
import pandas as pd

os.makedirs("data/processed", exist_ok=True)

print("📂 Reading raw data...")
tx     = pd.read_csv("data/raw/transactions.csv", parse_dates=["date"])
cust   = pd.read_csv("data/raw/customers.csv",    parse_dates=["signup_date"])
prod   = pd.read_csv("data/raw/products.csv")
stores = pd.read_csv("data/raw/stores.csv")

# ---------------------------------------------------------
# CLEANING
# ---------------------------------------------------------
print("🧹 Cleaning...")
before = len(tx)
tx = tx.drop_duplicates()
tx = tx.dropna(subset=["customer_id", "product_id", "revenue"])
tx = tx[tx["revenue"] > 0]
tx = tx[tx["quantity"] > 0]
print(f"   Removed {before - len(tx):,} bad rows")

# Type casting
tx["customer_id"] = tx["customer_id"].astype(int)
tx["product_id"] = tx["product_id"].astype(int)
tx["store_id"]   = tx["store_id"].astype(int)

# ---------------------------------------------------------
# FEATURE ENGINEERING
# ---------------------------------------------------------
print("✨ Feature engineering...")
tx["profit"]     = tx["revenue"] - tx["cost"]
tx["margin_pct"] = (tx["profit"] / tx["revenue"]).round(4)
tx["year"]       = tx["date"].dt.year
tx["month"]      = tx["date"].dt.to_period("M").astype(str)
tx["quarter"]    = tx["date"].dt.to_period("Q").astype(str)
tx["weekday"]    = tx["date"].dt.day_name()
tx["is_weekend"] = tx["date"].dt.dayofweek.isin([5, 6])

# Customer age bucket
cust["age_bucket"] = pd.cut(
    cust["age"],
    bins=[17, 25, 35, 50, 70],
    labels=["18-25", "26-35", "36-50", "51-70"],
)

# ---------------------------------------------------------
# JOIN -> FACT TABLE
# ---------------------------------------------------------
print("🔗 Joining...")
fact = (
    tx
    .merge(prod,   on="product_id", how="left", suffixes=("", "_prod"))
    .merge(stores, on="store_id",   how="left", suffixes=("", "_store"))
    .merge(cust,   on="customer_id",how="left", suffixes=("", "_cust"))
)

# Standardize region column (prefer customer region)
if "region" in fact.columns and "region_store" in fact.columns:
    fact["region"] = fact["region"].fillna(fact["region_store"])

fact.to_parquet("data/processed/fact_sales.parquet", index=False)

print(f"
✅ Clean fact table saved: {fact.shape[0]:,} rows x {fact.shape[1]} cols")
print(f"   Date range: {fact['date'].min().date()} -> {fact['date'].max().date()}")
print(f"   Total revenue: ₹{fact['revenue'].sum():,.0f}")
print(f"   Unique customers: {fact['customer_id'].nunique():,}")
