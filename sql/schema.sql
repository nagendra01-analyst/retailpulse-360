-- =====================================================
-- RetailPulse 360 - Star Schema for Retail Analytics
-- =====================================================
-- Designed for PostgreSQL 14+. Indexed for the most
-- common executive query patterns.
-- =====================================================

DROP TABLE IF EXISTS transactions CASCADE;
DROP TABLE IF EXISTS inventory    CASCADE;
DROP TABLE IF EXISTS customers    CASCADE;
DROP TABLE IF EXISTS products     CASCADE;
DROP TABLE IF EXISTS stores       CASCADE;

-- ----------------------------
-- DIM: Customers
-- ----------------------------
CREATE TABLE customers (
    customer_id   INT PRIMARY KEY,
    name          VARCHAR(100),
    email         VARCHAR(120),
    city          VARCHAR(50),
    region        VARCHAR(20),
    signup_date   DATE,
    age           INT,
    gender        VARCHAR(10),
    loyalty_tier  VARCHAR(20)
);

-- ----------------------------
-- DIM: Products
-- ----------------------------
CREATE TABLE products (
    product_id    INT PRIMARY KEY,
    product_name  VARCHAR(150),
    category      VARCHAR(50),
    unit_price    NUMERIC(10, 2),
    cost          NUMERIC(10, 2)
);

-- ----------------------------
-- DIM: Stores
-- ----------------------------
CREATE TABLE stores (
    store_id    INT PRIMARY KEY,
    store_name  VARCHAR(120),
    region      VARCHAR(20),
    channel     VARCHAR(20)
);

-- ----------------------------
-- FACT: Transactions
-- ----------------------------
CREATE TABLE transactions (
    transaction_id BIGINT PRIMARY KEY,
    customer_id    INT REFERENCES customers(customer_id),
    product_id     INT REFERENCES products(product_id),
    store_id       INT REFERENCES stores(store_id),
    date           DATE NOT NULL,
    quantity       INT,
    discount       NUMERIC(4, 2),
    revenue        NUMERIC(12, 2),
    cost           NUMERIC(12, 2)
);

-- ----------------------------
-- FACT: Inventory snapshot
-- ----------------------------
CREATE TABLE inventory (
    store_id       INT REFERENCES stores(store_id),
    product_id     INT REFERENCES products(product_id),
    stock_qty      INT,
    reorder_level  INT,
    PRIMARY KEY (store_id, product_id)
);

-- ----------------------------
-- INDEXES (query performance)
-- ----------------------------
CREATE INDEX idx_txn_date     ON transactions(date);
CREATE INDEX idx_txn_customer ON transactions(customer_id);
CREATE INDEX idx_txn_product  ON transactions(product_id);
CREATE INDEX idx_txn_store    ON transactions(store_id);
CREATE INDEX idx_cust_region  ON customers(region);
CREATE INDEX idx_prod_cat     ON products(category);
