# 🏗️ Architecture - RetailPulse 360

## High-Level Diagram (ASCII)

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  RAW SOURCES │──▶│  ETL (Python)│──▶│  POSTGRESQL  │
│ CSV / API/POS│   │ pandas+SQLAlc│   │ Star Schema  │
└──────────────┘   └──────────────┘   └─────┬───────┘
                                          │
        ┌────────────────────────────────┼──────────────┐
        ▼                              ▼                  ▼
┌──────────────┐            ┌──────────────┐   ┌──────────────┐
│  ML LAYER    │            │  KPI ENGINE  │   │   POWER BI   │
│ Prophet / XGB│            │  Python+SQL  │   │  Dashboards  │
│ KMeans (RFM) │            └─────┬───────┘   └─────┬───────┘
└─────┬───────┘                  │                 │
      ▼                          ▼                 ▼
┌─────────────────────────────────────────────────┐
│        STREAMLIT EXECUTIVE DASHBOARD                    │
│ KPIs · Forecasts · Segments · AI Recommendations        │
└────────────────────────────────────────────────┘
```

## Layer Breakdown

### 1. Ingestion
Sources include POS systems, e-commerce APIs, marketing platforms and a CRM. Synthetic generator (`src/01_generate_data.py`) produces equivalent CSVs locally for demo/dev.

### 2. Storage
PostgreSQL star schema with one fact (`transactions`) and four dimensions (`customers`, `products`, `stores`, `inventory`). Indexed on date, customer and product for sub-second query latency.

### 3. Transformation
Python pipeline (`src/02_clean_transform.py`) handles deduplication, type-casting, derived metrics (profit, margin, weekday), and writes a Parquet fact table for fast columnar analytics.

### 4. Analytics & ML
- **KPI engine** — 15+ executive KPIs computed via SQL + pandas
- **Forecasting** — Prophet daily revenue model, 90-day horizon
- **Segmentation** — RFM + KMeans (4 personas)
- **Churn** — XGBoost classifier, AUC > 0.90
- **Prescriptive AI** — rule-based recommendation engine (LLM-ready)

### 5. Visualization
- **Power BI** for multi-page executive dashboard (drill-through, slicers)
- **Streamlit** for interactive web app (modern dark UI, glassmorphism cards)
- **Plotly** for embeddable HTML charts

## Tech Choices Justified

| Decision | Why |
|---|---|
| PostgreSQL | Open-source, ACID, window functions for cohort/RFM |
| Parquet | Columnar compression → 10x faster pandas reads |
| Prophet | Robust to missing data, strong with weekly+yearly seasonality |
| XGBoost | Best-in-class for tabular data, handles imbalanced classes |
| Streamlit | Pure-Python rapid prototyping, deploys in minutes |
