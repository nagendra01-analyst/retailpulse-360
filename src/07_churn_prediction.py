"""
RetailPulse 360 - Churn Prediction (XGBoost)
----------------------------------------------
Labels customers as 'churned' if their last purchase
was > 90 days ago, then trains an XGBoost binary
classifier on RFM features and produces a churn
probability for every customer.

Output: data/processed/customer_churn.csv
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics         import classification_report, roc_auc_score
from xgboost                  import XGBClassifier

rfm = pd.read_csv("data/processed/rfm_segments.csv")
rfm["churn"] = (rfm["Recency"] > 90).astype(int)

FEATURES = ["Recency", "Frequency", "Monetary"]
X, y = rfm[FEATURES], rfm["churn"]

X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

clf = XGBClassifier(
    n_estimators=300,
    max_depth=4,
    learning_rate=0.08,
    eval_metric="auc",
    use_label_encoder=False,
    random_state=42,
)
clf.fit(X_tr, y_tr)

preds = clf.predict(X_te)
proba = clf.predict_proba(X_te)[:, 1]

print("=" * 50)
print("  CHURN MODEL EVALUATION")
print("=" * 50)
print(classification_report(y_te, preds, digits=3))
print(f"  ROC-AUC: {roc_auc_score(y_te, proba):.4f}")
print("=" * 50)

rfm["churn_probability"] = clf.predict_proba(X)[:, 1]
rfm["risk_band"] = pd.cut(
    rfm["churn_probability"],
    bins=[-0.01, 0.3, 0.6, 1.01],
    labels=["Low", "Medium", "High"],
)
rfm.to_csv("data/processed/customer_churn.csv", index=False)

print(f"
✅ Saved churn scores for {len(rfm):,} customers")
print(rfm["risk_band"].value_counts())
