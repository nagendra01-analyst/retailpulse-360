-- =====================================================
-- RetailPulse 360 - Executive KPI Queries
-- =====================================================

-- 1. Monthly revenue & profit trend
SELECT
    DATE_TRUNC('month', date)        AS month,
    SUM(revenue)                     AS revenue,
    SUM(revenue - cost)              AS profit,
    ROUND(SUM(revenue - cost) * 100.0 / NULLIF(SUM(revenue), 0), 2) AS margin_pct
FROM transactions
GROUP BY 1
ORDER BY 1;

-- 2. Top 10 customers by lifetime value
SELECT
    c.customer_id,
    c.name,
    SUM(t.revenue)                   AS lifetime_value,
    COUNT(DISTINCT t.transaction_id) AS total_orders,
    ROUND(AVG(t.revenue), 2)         AS avg_order_value
FROM transactions t
JOIN customers    c USING (customer_id)
GROUP BY c.customer_id, c.name
ORDER BY lifetime_value DESC
LIMIT 10;

-- 3. Category profitability
SELECT
    p.category,
    SUM(t.revenue)                                                  AS revenue,
    SUM(t.revenue - t.cost)                                         AS profit,
    ROUND(SUM(t.revenue - t.cost) * 100.0 / SUM(t.revenue), 2)      AS margin_pct,
    COUNT(DISTINCT t.transaction_id)                                AS orders
FROM transactions t
JOIN products    p USING (product_id)
GROUP BY p.category
ORDER BY profit DESC;

-- 4. Region x Channel performance
SELECT
    s.region,
    s.channel,
    SUM(t.revenue) AS revenue,
    COUNT(DISTINCT t.customer_id) AS customers
FROM transactions t
JOIN stores s USING (store_id)
GROUP BY s.region, s.channel
ORDER BY revenue DESC;

-- 5. Repeat purchase rate
SELECT
    ROUND(100.0 * COUNT(*) FILTER (WHERE orders > 1) / COUNT(*), 2) AS repeat_rate_pct
FROM (
    SELECT customer_id, COUNT(*) AS orders
    FROM transactions
    GROUP BY customer_id
) t;

-- 6. Average Order Value (AOV)
SELECT
    ROUND(AVG(order_value), 2) AS avg_order_value,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY order_value), 2) AS median_order_value
FROM (
    SELECT transaction_id, SUM(revenue) AS order_value
    FROM transactions
    GROUP BY transaction_id
) o;

-- 7. Inventory health (stockouts + low stock)
SELECT
    s.store_name,
    p.product_name,
    i.stock_qty,
    i.reorder_level,
    CASE
        WHEN i.stock_qty = 0                  THEN 'STOCKOUT'
        WHEN i.stock_qty < i.reorder_level    THEN 'LOW'
        ELSE 'OK'
    END AS status
FROM inventory i
JOIN stores   s USING (store_id)
JOIN products p USING (product_id)
WHERE i.stock_qty < i.reorder_level
ORDER BY i.stock_qty;

-- 8. Discount effectiveness (uplift on discounted vs full-price orders)
SELECT
    CASE WHEN discount > 0 THEN 'Discounted' ELSE 'Full Price' END AS bucket,
    COUNT(*)                       AS orders,
    ROUND(AVG(quantity), 2)        AS avg_qty,
    ROUND(AVG(revenue), 2)         AS avg_revenue
FROM transactions
GROUP BY 1;
