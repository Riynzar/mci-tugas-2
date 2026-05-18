-- ==========================================
-- DDL untuk ClickHouse
-- ==========================================

CREATE DATABASE IF NOT EXISTS analytics;

-- Tabel analitik unik per Produk
CREATE TABLE IF NOT EXISTS analytics.order_performance (
    product_name String,
    department String,
    total_sold Int32,
    unique_buyers Int32,
    total_reordered Int32,
    avg_order_dow Float64,
    avg_order_hour Float64,
    avg_days_since_prior Float64
) ENGINE = MergeTree()
ORDER BY (department, product_name);


-- ==========================================
-- Query SQL untuk Metabase (Visualisasi)
-- ==========================================

-- 1. Top 10 Produk Paling Laris
SELECT product_name, total_sold 
FROM analytics.order_performance 
ORDER BY total_sold DESC 
LIMIT 10;

-- 2. Rata-rata Waktu Pemesanan per Departemen
-- Menunjukkan apakah departemen tertentu cenderung dipesan pagi atau sore
SELECT department, AVG(avg_order_hour) as jam_rata_rata
FROM analytics.order_performance
GROUP BY department
ORDER BY jam_rata_rata;

-- 3. Rasio Reorder Produk (Mana produk yang bikin pelanggan ketagihan?)
SELECT product_name, (total_reordered / total_sold) * 100 as reorder_rate
FROM analytics.order_performance
WHERE total_sold > 2
ORDER BY reorder_rate DESC
LIMIT 15;

-- 4. Loyalitas Pelanggan (Berapa lama pelanggan kembali beli produk di dept tertentu?)
SELECT department, AVG(avg_days_since_prior) as rata_rata_hari_kembali
FROM analytics.order_performance
GROUP BY department
ORDER BY rata_rata_hari_kembali ASC;
