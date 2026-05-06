"""
RetailPulse 360 - RFM + KMeans Customer Segmentation
--------------------------------------------------------
Computes Recency, Frequency, Monetary scores per customer
and clusters them into 4 personas using KMeans:

  - Champions   : recent, frequent, high spend
  - Loyal       : moderate frequency, decent spend
  - At-Risk     : haven't purchased recently but spent well
  - Hibernating : low recency, frequency, monetary

Output: data/processed/rfm_segments.csv
"""
import pandas as pd
from sklearn.cluster   import KMeans
from sklearn.preprocessing import StandardScaler

fact = pd.read_parquet("data/processed/fact_sales.parquet")
fact["date"] = pd.to_datetime(fact["date"])
snapshot = fact["date"].max() + pd.Timedelta(days=1)

rfm = (
    fact.groupby("customer_id")
        .agg(
            Recency   = ("date",            lambda x: (snapshot - x.max()).days),
            Frequency = ("transaction_id",  "nunique"),
            Monetary  = ("revenue",         "sum"),
        )
        .reset_index()
)

# ---- Scale + cluster ----
X = StandardScaler().fit_transform(rfm[["Recency", "Frequency", "Monetary"]])
km = KMeans(n_clusters=4, random_state=42, n_init=10).fit(X)
rfm["cluster"] = km.labels_

# ---- Auto-label clusters by spend & recency ----
profile = (
    rfm.groupby("cluster")
       .agg(R=("Recency", "mean"), F=("Frequency", "mean"), M=("Monetary", "mean"))
       .reset_index()
)
profile = profile.sort_values("M", ascending=False).reset_index(drop=True)
labels  = ["Champions", "Loyal", "At-Risk", "Hibernating"]
label_map = dict(zip(profile["cluster"], labels))
rfm["segment"] = rfm["cluster"].map(label_map)

rfm.to_csv("data/processed/rfm_segments.csv", index=False)

summary = (
    rfm.groupby("segment")
       .agg(customers=("customer_id", "count"),
            avg_recency=("Recency",   "mean"),
            avg_frequency=("Frequency","mean"),
            total_revenue=("Monetary", "sum"))
       .round(2)
)
print("✅ Customer segmentation complete
")
print(summary)
