# 🛍️ RetailPulse 360 — AI-Powered Retail Analytics Platform

> An end-to-end enterprise analytics solution combining **SQL, Python, Power BI, and AI-driven forecasting** to deliver real-time business intelligence for omnichannel retail operations.

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-PostgreSQL-336791?logo=postgresql&logoColor=white)
![PowerBI](https://img.shields.io/badge/PowerBI-Dashboards-F2C811?logo=powerbi&logoColor=black)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![ML](https://img.shields.io/badge/ML-XGBoost%20%7C%20Prophet-orange)
![Status](https://img.shields.io/badge/Status-Production--Ready-success)
![License](https://img.shields.io/badge/License-MIT-blue)

---

## 🎯 Project Overview

**RetailPulse 360** transforms raw transactional retail data into actionable executive insights for *NovaMart*, a fictional mid-sized omnichannel retailer (50+ stores, 4 regions, 5,000+ customers, 200K+ transactions).

It covers the full analytics lifecycle:

- **Data Engineering** — synthetic data generation + ETL pipelines
- **Data Cleaning & Transformation** — deduplication, type casting, derived KPIs
- **Exploratory & Diagnostic Analytics** — SQL + pandas
- **Predictive Analytics** — Prophet 90-day sales forecast, XGBoost churn prediction
- **Customer Segmentation** — RFM + KMeans (4 personas)
- **Prescriptive AI** — rule-based recommendation engine
- **Visualization** — Power BI executive dashboard + Streamlit app with modern dark UI

---

## 🧠 Tech Stack

| Layer | Tools |
|---|---|
| **Languages** | Python 3.11, SQL (PostgreSQL) |
| **Data** | pandas, NumPy, Faker, SQLAlchemy |
| **ML / AI** | scikit-learn, XGBoost, Prophet |
| **Visualization** | Power BI, Plotly, Streamlit |
| **Infra** | PostgreSQL, Parquet |

---

## 🚀 Quick Start

```bash
git clone https://github.com/nagendra01-analyst/retailpulse-360.git
cd retailpulse-360
pip install -r requirements.txt

python src/01_generate_data.py
python src/02_clean_transform.py
python src/04_kpi_engine.py
python src/05_forecasting_prophet.py
python src/06_customer_segmentation.py
python src/07_churn_prediction.py
python src/08_ai_recommendations.py

streamlit run dashboards/streamlit_app.py
```

---

## 📊 Key Features

- **15+ Executive KPIs** — Revenue, Profit, Gross Margin, AOV, CLTV, Repeat Rate, Inventory Turnover, Churn %
- **Interactive Streamlit Dashboard** — modern dark UI, glassmorphism cards, responsive filters
- **Power BI Executive Dashboard** — multi-page with drill-through and slicers
- **90-Day Sales Forecast** — Prophet model with confidence intervals
- **RFM Customer Segmentation** — 4 personas: Champions, Loyal, At-Risk, Hibernating
- **Churn Prediction** — XGBoost classifier with AUC > 0.90
- **AI-Generated Recommendations** — prescriptive insights for marketing, inventory, retention

---

## 📈 Business Impact (Simulated)

| Metric | Result |
|---|---|
| 📉 Stockout reduction | **↓12%** |
| 💰 Marketing ROI lift | **↑23%** |
| 🔮 Forecast accuracy (MAPE) | **6.4%** |
| 🎯 Revenue at risk identified | **$1.8M** |
| ⏱️ Reporting time saved | **↓85%** (manual → automated) |

---

## 📂 Folder Structure

```
retailpulse-360/
├── src/                  # Python pipeline scripts
├── sql/                  # SQL schema + analytical queries
├── dashboards/           # Streamlit + Power BI assets
├── docs/                 # Architecture, KPIs, business impact, interview Q&A
├── data/                 # raw + processed (gitignored)
├── requirements.txt
└── README.md
```

See `docs/` for architecture diagram, KPI definitions, business impact, and interview prep.

---

## 👤 Author

**Nagendra** — Senior Data Analyst  
🔗 [GitHub](https://github.com/nagendra01-analyst)

---

## 📄 License

MIT © 2026 Nagendra
