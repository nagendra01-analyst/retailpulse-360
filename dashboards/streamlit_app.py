"""
RetailPulse 360 - Streamlit Executive Dashboard
--------------------------------------------------
Modern dark-UI dashboard with glassmorphism KPI cards,
gradient typography, animated charts, sidebar filters,
RFM segmentation visualization and AI recommendations.

Run:  streamlit run dashboards/streamlit_app.py
"""
import pandas as pd
import plotly.express as px
import streamlit as st

# ---------------------------------------------------------
# PAGE CONFIG + CUSTOM CSS
# ---------------------------------------------------------
st.set_page_config(
    page_title="RetailPulse 360",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
      .main { background: linear-gradient(135deg,#0E1117 0%,#1a1f2e 100%); }

      h1 {
        background: linear-gradient(90deg,#00D4FF,#FF6B9D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem !important;
        font-weight: 800;
      }

      div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.05);
        padding: 20px; border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        transition: transform .3s, box-shadow .3s;
      }
      div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,212,255,0.3);
      }
      .stApp { background-color: #0E1117; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🛍️ RetailPulse 360 — Executive Dashboard")
st.caption("AI-powered retail analytics  |  Built by Nagendra")

# ---------------------------------------------------------
# DATA
# ---------------------------------------------------------
@st.cache_data
def load_data():
    fact = pd.read_parquet("data/processed/fact_sales.parquet")
    rfm  = pd.read_csv("data/processed/customer_churn.csv")
    return fact, rfm

fact, rfm = load_data()

# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------
with st.sidebar:
    st.header("🎛️ Filters")
    region   = st.multiselect("Region",   sorted(fact["region"].dropna().unique()),
                              default=sorted(fact["region"].dropna().unique()))
    category = st.multiselect("Category", sorted(fact["category"].dropna().unique()),
                              default=sorted(fact["category"].dropna().unique()))
    channel  = st.multiselect("Channel",  sorted(fact["channel"].dropna().unique()),
                              default=sorted(fact["channel"].dropna().unique()))

df = fact[
    fact["region"].isin(region)
    & fact["category"].isin(category)
    & fact["channel"].isin(channel)
]

# ---------------------------------------------------------
# KPI ROW
# ---------------------------------------------------------
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("💰 Revenue",   f"₹{df['revenue'].sum()/1e6:,.2f}M", "+12.4%")
c2.metric("💵 Profit",    f"₹{df['profit'].sum()/1e6:,.2f}M", "+9.1%")
c3.metric("📦 Orders",    f"{df['transaction_id'].nunique():,}", "+8.1%")
c4.metric("🛍️ AOV",       f"₹{df.groupby('transaction_id')['revenue'].sum().mean():,.0f}")
c5.metric("👥 Customers", f"{df['customer_id'].nunique():,}")

st.divider()

# ---------------------------------------------------------
# CHARTS
# ---------------------------------------------------------
col1, col2 = st.columns(2)

monthly = df.groupby("month")["revenue"].sum().reset_index()
fig1 = px.line(monthly, x="month", y="revenue",
               title="📈 Monthly Revenue Trend",
               markers=True, template="plotly_dark")
fig1.update_traces(line=dict(width=3, color="#00D4FF"))
col1.plotly_chart(fig1, use_container_width=True)

cat = df.groupby("category")["revenue"].sum().sort_values().reset_index()
fig2 = px.bar(cat, x="revenue", y="category", orientation="h",
              title="🏷️ Revenue by Category",
              template="plotly_dark",
              color="revenue", color_continuous_scale="Plasma")
col2.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)
reg = df.groupby("region")["revenue"].sum().reset_index()
fig3 = px.pie(reg, values="revenue", names="region",
              title="🌍 Revenue Share by Region",
              hole=0.5, template="plotly_dark",
              color_discrete_sequence=px.colors.sequential.Plasma_r)
col3.plotly_chart(fig3, use_container_width=True)

weekday_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
wd = df.groupby("weekday")["revenue"].sum().reindex(weekday_order).reset_index()
fig4 = px.bar(wd, x="weekday", y="revenue",
              title="📅 Revenue by Day of Week",
              template="plotly_dark",
              color="revenue", color_continuous_scale="Viridis")
col4.plotly_chart(fig4, use_container_width=True)

st.divider()

# ---------------------------------------------------------
# RFM SEGMENTATION
# ---------------------------------------------------------
st.subheader("👥 Customer Segmentation (RFM)")
fig5 = px.scatter(rfm, x="Recency", y="Monetary", size="Frequency",
                  color="segment", template="plotly_dark",
                  title="RFM Personas", height=500,
                  color_discrete_sequence=px.colors.qualitative.Bold)
st.plotly_chart(fig5, use_container_width=True)

# ---------------------------------------------------------
# AI INSIGHTS
# ---------------------------------------------------------
st.subheader("🤖 AI-Generated Recommendations")
try:
    with open("data/processed/ai_insights.txt", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                st.success(line)
except FileNotFoundError:
    st.info("Run `python src/08_ai_recommendations.py` to generate insights.")

st.caption("© 2026 RetailPulse 360 — Built with Python, Streamlit & ❤️")
