-- =====================================================
-- RetailPulse 360 - Cohort Retention Analysis
-- =====================================================
-- Builds a monthly cohort matrix showing how many
-- customers from each acquisition month remain active
-- in subsequent months (classic retention curve).
-- =====================================================

WITH first_order AS (
    SELECT
        customer_id,
        DATE_TRUNC('month', MIN(date)) AS cohort_month
    FROM transactions
    GROUP BY customer_id
),
activity AS (
    SELECT
        f.cohort_month,
        DATE_TRUNC('month', t.date) AS activity_month,
        t.customer_id
    FROM transactions t
    JOIN first_order  f USING (customer_id)
),
cohort_matrix AS (
    SELECT
        cohort_month,
        activity_month,
        EXTRACT(YEAR  FROM AGE(activity_month, cohort_month)) * 12
      + EXTRACT(MONTH FROM AGE(activity_month, cohort_month))    AS month_number,
        COUNT(DISTINCT customer_id)                               AS active_customers
    FROM activity
    GROUP BY cohort_month, activity_month
)
SELECT
    cohort_month,
    month_number,
    active_customers,
    ROUND(
        100.0 * active_customers /
        FIRST_VALUE(active_customers) OVER (
            PARTITION BY cohort_month ORDER BY month_number
        ), 2
    ) AS retention_pct
FROM cohort_matrix
ORDER BY cohort_month, month_number;
