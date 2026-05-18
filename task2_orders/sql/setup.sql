-- 1. Total Produk Terjual
SELECT sum(total_sold) FROM analytics.order_performance;

-- 2. Total Produk
SELECT count(DISTINCT product_name) FROM analytics.order_performance;

-- 3. Total Departemen
SELECT count(DISTINCT department) FROM analytics.order_performance

-- 4. Rush Day
SELECT 
    CASE 
        WHEN FLOOR(avg_order_dow + 0.5) <= 0 THEN 'Minggu'
        WHEN FLOOR(avg_order_dow + 0.5) = 1 THEN 'Senin'
        WHEN FLOOR(avg_order_dow + 0.5) = 2 THEN 'Selasa'
        WHEN FLOOR(avg_order_dow + 0.5) = 3 THEN 'Rabu'
        WHEN FLOOR(avg_order_dow + 0.5) = 4 THEN 'Kamis'
        WHEN FLOOR(avg_order_dow + 0.5) = 5 THEN 'Jumat'
        ELSE 'Sabtu'
    END AS hari_paling_ramai,
    COUNT(*) AS jumlah_distribusi
FROM 
    analytics.order_performance
GROUP BY 
    1
ORDER BY 
    jumlah_distribusi DESC;

-- 5. Top 10 Produk Terlaris
SELECT product_name, total_sold 
FROM analytics.order_performance 
ORDER BY total_sold DESC 
LIMIT 10;

-- 6. Rush Hour per Departemen
SELECT department, AVG(avg_order_hour) as jam_rata_rata
FROM analytics.order_performance
GROUP BY department
ORDER BY jam_rata_rata;

-- 7. Produk Paling Banyak Reorder
SELECT product_name, total_reordered
FROM analytics.order_performance
ORDER BY total_reordered DESC
LIMIT 5;

-- 8. Produk dengan Daya Tarik Terluas
SELECT 
    product_name, 
    unique_buyers
FROM analytics.order_performance
ORDER BY unique_buyers DESC
LIMIT 5;

-- 9. Rata-rata Loyalitas Pelanggan per Departemen
SELECT department, AVG(avg_days_since_prior) as rata_rata_hari_kembali
FROM analytics.order_performance
WHERE avg_days_since_prior > 0
GROUP BY department
ORDER BY rata_rata_hari_kembali ASC;



