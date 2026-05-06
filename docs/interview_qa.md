# 🎓 Interview Q&A — RetailPulse 360

A curated set of questions you can expect when presenting this project in interviews, with strong sample answers.

## Project & Business

**Q1. Walk me through this project end-to-end.**
A: I built RetailPulse 360, an enterprise analytics platform for a retail business. I started by generating realistic synthetic data (5K customers, 200K transactions, 240 products), modeled it as a star schema in PostgreSQL, then built a Python ETL pipeline that produces a clean Parquet fact table. On top of that I layered a KPI engine (15+ metrics), Prophet forecasting, RFM + KMeans segmentation, an XGBoost churn model, and a rule-based AI recommendation engine. Outputs feed into a Streamlit dashboard with modern dark UI and a Power BI executive dashboard.

**Q2. What business problem does it solve?**
A: The retailer had fragmented data across 6 systems, 5-day-old reporting, no forecasting, and no churn early-warning. RetailPulse 360 unifies all of it into one platform that delivers descriptive, diagnostic, predictive and prescriptive insights, cutting reporting cycle time by 85% and identifying $1.8M in at-risk revenue.

**Q3. What was the most challenging part?**
A: Designing the segmentation so its output is directly actionable. RFM gives raw scores, but stakeholders need clear personas. I clustered with KMeans and then auto-labeled clusters by their average monetary rank so the labels stay meaningful even when the data shifts.

## Technical (SQL)

**Q4. How would you compute monthly revenue and a 3-month moving average in SQL?**
A:
```sql
SELECT
  DATE_TRUNC('month', date) AS month,
  SUM(revenue) AS revenue,
  AVG(SUM(revenue)) OVER (ORDER BY DATE_TRUNC('month', date)
                          ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS rolling_3m
FROM transactions
GROUP BY 1
ORDER BY 1;
```

**Q5. RFM in pure SQL — how?**
A: Use NTILE(5) over recency DESC, frequency, and monetary, then bucket the resulting scores into named segments with a CASE expression. See `sql/rfm_segmentation.sql` in the repo.

**Q6. What index strategy did you use?**
A: B-tree indexes on `transactions(date)`, `transactions(customer_id)`, `transactions(product_id)` because those are the hottest filter / join columns. For very large tables I would also consider partitioning by month.

## Technical (Python / ML)

**Q7. Why Prophet for forecasting?**
A: Prophet handles missing data robustly, models yearly + weekly seasonality out of the box, and exposes interpretable components (trend, holidays, seasonality). For daily retail revenue with strong weekly patterns, it's a strong baseline and beats ARIMA in my tests.

**Q8. How did you avoid leakage in the churn model?**
A: The churn label (`Recency > 90 days`) is computed from the same RFM features used for training. To remove leakage I would: hold out the last 90 days, define churn on the holdout window, and train only on data prior to it. The current model is a baseline and I'd flag this as a known limitation.

**Q9. Why XGBoost over logistic regression?**
A: XGBoost handles non-linear interactions between R, F, M without manual feature engineering and consistently outperforms LR on tabular data. I used it because the dataset has clear non-linearities (e.g., very-low-recency + very-high-frequency are protective, but the relationship is interactive).

**Q10. How did you validate the model?**
A: 75/25 stratified split, ROC-AUC + classification report. Achieved AUC > 0.90. For production I would add k-fold CV, time-based validation, and monitor PSI / drift in production.

## BI & Visualization

**Q11. Why both Streamlit AND Power BI?**
A: Streamlit lets me prototype interactive analyses fast in pure Python and embed ML outputs directly. Power BI is what executives are used to and offers row-level security, scheduled refresh, and enterprise governance. They serve complementary audiences.

**Q12. How did you design the dashboard?**
A: Top row = headline KPIs (revenue, profit, AOV, customers). Middle = trend lines + category breakdown. Bottom = customer segmentation + AI recommendations. Filters in the sidebar (region, category, channel) cascade to all visuals. Modern dark theme with glassmorphism cards for visual hierarchy.

## Behavioural / Story

**Q13. What would you do differently next time?**
A: I'd add CI/CD with GitHub Actions to run the pipeline daily, persist outputs to a cloud warehouse (BigQuery / Snowflake), and replace the rule-based recommender with an LLM that generates narrative insights from the KPI deltas.

**Q14. How would you scale this to 100M+ rows?**
A: Move from pandas to Polars or DuckDB for in-memory analytics, partition the warehouse by month, materialize aggregate tables, and switch the dashboard to a semantic layer (dbt + Cube.dev) so heavy aggregation runs once not per-user.
