"""
RetailPulse 360 - AI Recommendation Engine
--------------------------------------------
Generates prescriptive business recommendations
based on the analytical outputs (KPIs, RFM,
churn scores, forecast).

Swap the rule-based generator with an OpenAI / Claude
API call to upgrade to true LLM-generated narrative.

Output: data/processed/ai_insights.txt
"""
import os
import pandas as pd

fact = pd.read_parquet("data/processed/fact_sales.parquet")
rfm  = pd.read_csv("data/processed/customer_churn.csv")
fcst = pd.read_csv("data/processed/forecast.csv")

# ---- Diagnose key signals ----
top_cat       = fact.groupby("category")["revenue"].sum().idxmax()
worst_region  = fact.groupby("region")["revenue"].sum().idxmin()
best_region   = fact.groupby("region")["revenue"].sum().idxmax()
high_risk     = (rfm["churn_probability"] > 0.7).sum()
rev_at_risk   = rfm.loc[rfm["churn_probability"] > 0.7, "Monetary"].sum()
champions     = (rfm["segment"] == "Champions").sum()
fcst_total    = fcst["yhat"].sum()
weekend_share = fact.loc[fact["is_weekend"], "revenue"].sum() / fact["revenue"].sum() * 100
online_share  = fact.loc[fact["channel"] == "Online", "revenue"].sum() / fact["revenue"].sum() * 100

insights = [
    f"🏆 [GROWTH] '{top_cat}' is the #1 revenue category. Increase paid-media spend by 15% and feature in homepage hero.",
    f"⚠️  [REGION] '{worst_region}' region underperforms vs '{best_region}'. Launch a 4-week regional promo with 10% discount on top SKUs.",
    f"🚨 [RETENTION] {high_risk:,} customers have >70% churn probability, representing ₹{rev_at_risk:,.0f} of historical revenue. Trigger a 3-touch win-back email + WhatsApp sequence.",
    f"💎 [LOYALTY] {champions:,} customers are 'Champions'. Offer early-access drops + referral bonus to amplify LTV.",
    f"📈 [FORECAST] Next 90 days projected revenue: ₹{fcst_total:,.0f}. Align inventory + workforce planning accordingly.",
    f"🛍️ [CHANNEL] Online channel drives {online_share:.1f}% of revenue. Invest in CRO + checkout optimization for highest ROI.",
    f"📅 [TIMING] {weekend_share:.1f}% of revenue happens on weekends. Schedule push notifications + flash sales Fri-Sun evenings.",
    f"📦 [INVENTORY] Raise auto-reorder thresholds by 20% for top-quartile SKUs to reduce stockouts.",
    f"💰 [PRICING] Test a +3% price lift on inelastic top-SKUs to expand gross margin without volume loss.",
    f"🔍 [SEGMENT] Personalize email subject lines per RFM segment - Champions respond to exclusivity, At-Risk to discounts.",
]

os.makedirs("data/processed", exist_ok=True)
with open("data/processed/ai_insights.txt", "w", encoding="utf-8") as f:
    f.write("
".join(insights))

print("=" * 60)
print("  AI-GENERATED BUSINESS RECOMMENDATIONS")
print("=" * 60)
for i, line in enumerate(insights, 1):
    print(f"{i:2d}. {line}")
print("=" * 60)
