"""
RetailPulse 360 - 90-Day Sales Forecast (Prophet)
----------------------------------------------------
Uses Facebook Prophet to model daily revenue with
yearly + weekly seasonality and produces a 90-day
forward forecast with 95% confidence intervals.

Outputs:
  - data/processed/forecast.csv  (next 90 days)
  - dashboards/screenshots/forecast.html (interactive Plotly)
"""
import os
import pandas as pd
import plotly.graph_objects as go
from prophet import Prophet

os.makedirs("dashboards/screenshots", exist_ok=True)
os.makedirs("data/processed",         exist_ok=True)

fact = pd.read_parquet("data/processed/fact_sales.parquet")

daily = (
    fact.groupby("date")["revenue"].sum()
    .reset_index()
    .rename(columns={"date": "ds", "revenue": "y"})
)
daily["ds"] = pd.to_datetime(daily["ds"])
print(f"📊 Training Prophet on {len(daily)} daily observations...")

m = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False,
    interval_width=0.95,
)
m.fit(daily)

future = m.make_future_dataframe(periods=90)
fcst   = m.predict(future)

# Save next 90 days
fcst[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(90).to_csv(
    "data/processed/forecast.csv", index=False
)

# ---------------- Plot ----------------
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=daily["ds"], y=daily["y"],
    name="Actual Revenue",
    line=dict(color="#00D4FF", width=2),
))
fig.add_trace(go.Scatter(
    x=fcst["ds"], y=fcst["yhat"],
    name="Forecast",
    line=dict(color="#FF6B9D", width=2, dash="dash"),
))
fig.add_trace(go.Scatter(
    x=fcst["ds"], y=fcst["yhat_upper"],
    line=dict(width=0), showlegend=False, hoverinfo="skip",
))
fig.add_trace(go.Scatter(
    x=fcst["ds"], y=fcst["yhat_lower"],
    fill="tonexty", line=dict(width=0),
    name="95% Confidence",
    fillcolor="rgba(255,107,157,0.2)",
))
fig.update_layout(
    template="plotly_dark",
    title="📈 RetailPulse 360 - 90-Day Revenue Forecast",
    xaxis_title="Date",
    yaxis_title="Revenue (₹)",
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    hovermode="x unified",
)
fig.write_html("dashboards/screenshots/forecast.html")

# ---------------- Accuracy (in-sample) ----------------
merged = daily.merge(fcst[["ds", "yhat"]], on="ds", how="left")
mape = ((merged["y"] - merged["yhat"]).abs() / merged["y"]).mean() * 100
print(f"✅ Forecast saved. In-sample MAPE: {mape:.2f}%")
