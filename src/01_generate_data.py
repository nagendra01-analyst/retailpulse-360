"""
RetailPulse 360 - Synthetic Data Generator
--------------------------------------------
Generates realistic retail transactional data:
  - 5,000 customers across 4 regions
  - 240 products across 6 categories
  - 50 stores (online + offline)
  - 200,000 transactions over 2 years
  - Inventory snapshot per store-product

Output: data/raw/*.csv
"""
import os
import random
import numpy as np
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()
np.random.seed(42)
random.seed(42)
Faker.seed(42)

os.makedirs("data/raw", exist_ok=True)

# ---------------------------------------------------------
# 1. CUSTOMERS
# ---------------------------------------------------------
N_CUSTOMERS = 5000
customers = pd.DataFrame({
    "customer_id": range(1, N_CUSTOMERS + 1),
    "name": [fake.name() for _ in range(N_CUSTOMERS)],
    "email": [fake.email() for _ in range(N_CUSTOMERS)],
    "city": np.random.choice(
        ["Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad", "Pune"],
        N_CUSTOMERS,
    ),
    "region": np.random.choice(["North", "South", "East", "West"], N_CUSTOMERS),
    "signup_date": [
        fake.date_between(start_date="-3y", end_date="-30d")
        for _ in range(N_CUSTOMERS)
    ],
    "age": np.random.randint(18, 70, N_CUSTOMERS),
    "gender": np.random.choice(["M", "F", "Other"], N_CUSTOMERS, p=[0.48, 0.49, 0.03]),
    "loyalty_tier": np.random.choice(
        ["Bronze", "Silver", "Gold", "Platinum"],
        N_CUSTOMERS, p=[0.5, 0.3, 0.15, 0.05],
    ),
})

# ---------------------------------------------------------
# 2. PRODUCTS
# ---------------------------------------------------------
categories = {
    "Electronics": (2000, 80000),
    "Apparel":     (500,  5000),
    "Grocery":     (50,   2000),
    "Home":        (800,  15000),
    "Beauty":      (200,  3000),
    "Sports":      (500,  10000),
}
products = []
pid = 1
for cat, (lo, hi) in categories.items():
    for _ in range(40):
        price = round(np.random.uniform(lo, hi), 2)
        cost  = round(price * np.random.uniform(0.45, 0.7), 2)
        products.append({
            "product_id": pid,
            "product_name": f"{cat}-{fake.word().title()}-{pid}",
            "category": cat,
            "unit_price": price,
            "cost": cost,
        })
        pid += 1
products = pd.DataFrame(products)

# ---------------------------------------------------------
# 3. STORES
# ---------------------------------------------------------
stores = pd.DataFrame({
    "store_id":   range(1, 51),
    "store_name": [f"NovaMart-{fake.city()}" for _ in range(50)],
    "region":     np.random.choice(["North", "South", "East", "West"], 50),
    "channel":    np.random.choice(["Online", "Offline"], 50, p=[0.3, 0.7]),
})

# ---------------------------------------------------------
# 4. TRANSACTIONS (2 years)
# ---------------------------------------------------------
N_TXN = 200_000
start = datetime.now() - timedelta(days=730)
txns = []
for i in range(N_TXN):
    d = start + timedelta(
        days=np.random.randint(0, 730),
        hours=int(np.random.randint(0, 24)),
    )
    cust = int(np.random.randint(1, N_CUSTOMERS + 1))
    prod = products.sample(1).iloc[0]
    qty = int(np.random.choice(
        [1, 1, 1, 2, 2, 3, 4, 5],
        p=[0.4, 0.2, 0.1, 0.1, 0.08, 0.05, 0.04, 0.03],
    ))
    discount = float(np.random.choice(
        [0, 0, 0, 0.05, 0.1, 0.15, 0.2],
        p=[0.5, 0.15, 0.1, 0.1, 0.07, 0.05, 0.03],
    ))
    revenue = round(prod.unit_price * qty * (1 - discount), 2)
    cost = round(prod.cost * qty, 2)
    txns.append({
        "transaction_id": i + 1,
        "customer_id": cust,
        "product_id": int(prod.product_id),
        "store_id": int(np.random.randint(1, 51)),
        "date": d.date(),
        "quantity": qty,
        "discount": discount,
        "revenue": revenue,
        "cost": cost,
    })
transactions = pd.DataFrame(txns)

# ---------------------------------------------------------
# 5. INVENTORY (store x product snapshot)
# ---------------------------------------------------------
inventory = pd.DataFrame([
    {
        "store_id": s,
        "product_id": p,
        "stock_qty": int(np.random.randint(0, 300)),
        "reorder_level": int(np.random.randint(20, 80)),
    }
    for s in range(1, 51)
    for p in products.product_id
])

# ---------------------------------------------------------
# SAVE
# ---------------------------------------------------------
customers.to_csv("data/raw/customers.csv", index=False)
products.to_csv("data/raw/products.csv", index=False)
stores.to_csv("data/raw/stores.csv", index=False)
transactions.to_csv("data/raw/transactions.csv", index=False)
inventory.to_csv("data/raw/inventory.csv", index=False)

print(f"✅ Generated {len(transactions):,} transactions")
print(f"   - {len(customers):,} customers")
print(f"   - {len(products):,} products")
print(f"   - {len(stores):,} stores")
print(f"   - {len(inventory):,} inventory records")
