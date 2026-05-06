-- =====================================================
-- RetailPulse 360 - RFM Customer Segmentation (SQL)
-- =====================================================
-- Pure-SQL implementation of RFM scoring using NTILE.
-- Produces 5x5x5 = 125 raw scores -> bucketed into
-- 4 marketable segments.
-- =====================================================

WITH rfm AS (
    SELECT
        customer_id,
        (CURRENT_DATE - MAX(date))                  AS recency,
        COUNT(DISTINCT transaction_id)              AS frequency,
        SUM(revenue)                                AS monetary
    FROM transactions
    GROUP BY customer_id
),
scored AS (
    SELECT
        *,
        NTILE(5) OVER (ORDER BY recency DESC)       AS r_score,
        NTILE(5) OVER (ORDER BY frequency)          AS f_score,
        NTILE(5) OVER (ORDER BY monetary)           AS m_score
    FROM rfm
),
labeled AS (
    SELECT
        *,
        CASE
            WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
            WHEN r_score >= 3 AND f_score >= 3                  THEN 'Loyal'
            WHEN r_score <= 2 AND f_score >= 3                  THEN 'At-Risk'
            WHEN r_score <= 2 AND m_score >= 4                  THEN 'Cannot Lose Them'
            WHEN r_score >= 4 AND f_score <= 2                  THEN 'New / Promising'
            ELSE 'Hibernating'
        END AS segment
    FROM scored
)
SELECT
    segment,
    COUNT(*)                AS customers,
    ROUND(AVG(recency))     AS avg_recency_days,
    ROUND(AVG(frequency))   AS avg_frequency,
    ROUND(SUM(monetary), 2) AS total_revenue,
    ROUND(AVG(monetary), 2) AS avg_monetary
FROM labeled
GROUP BY segment
ORDER BY total_revenue DESC;
