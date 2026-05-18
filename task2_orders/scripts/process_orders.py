from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from clickhouse_driver import Client
import os
import glob
import sys

def run_orders_analytics():
    print("🚀 Memulai proses analisis Spark...")
    
    spark = SparkSession.builder \
        .appName("Orders_Analytics") \
        .config("spark.driver.memory", "1g") \
        .getOrCreate()

    input_path = "/opt/airflow/data_lake/orders/"
    
    # Cek apakah ada file csv untuk dibaca
    if not os.path.exists(input_path) or not glob.glob(f"{input_path}/*.csv"):
        print(f"⚠️ Tidak ditemukan file CSV di {input_path}. Melewati proses.")
        spark.stop()
        return

    try:
        print(f"📖 Membaca data CSV dari: {input_path}")
        # Membaca CSV dengan header dan infer schema
        df_raw = spark.read.option("header", "true").option("inferSchema", "true").csv(f"{input_path}/*.csv")

        print("📊 Menghitung metrik analitik produk (Unique per Product)...")
        # Grouping HANYA berdasarkan product_name dan department
        product_analysis = df_raw.groupBy("product_name", "department") \
            .agg(
                F.count("order_id").alias("total_sold"),
                F.countDistinct("user_id").alias("unique_buyers"),
                F.sum("reordered").alias("total_reordered"),
                F.avg("order_dow").alias("avg_order_dow"),
                F.avg("order_hour_of_day").alias("avg_order_hour"),
                F.avg("days_since_prior_order").alias("avg_days_since_prior")
            )

        final_results = product_analysis.toPandas()
        # Clean up nulls
        final_results['avg_days_since_prior'] = final_results['avg_days_since_prior'].fillna(0)
        
        print(f"✅ Analisis selesai. {len(final_results)} produk unik ditemukan.")
        spark.stop()

    except Exception as e:
        print(f"❌ Error saat pemrosesan Spark: {e}")
        spark.stop()
        sys.exit(1)

    print("💾 Menghubungkan ke ClickHouse...")
    try:
        client = Client(host='clickhouse-server', user='admin', password='rahasia')
        client.execute('CREATE DATABASE IF NOT EXISTS analytics')
        
        # Schema baru: Unik per Product + Department
        client.execute('''
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
            ORDER BY (department, product_name)
        ''')
        
        client.execute('TRUNCATE TABLE analytics.order_performance')
        data_tuples = [tuple(x) for x in final_results.to_numpy()]
        if data_tuples:
            client.execute('INSERT INTO analytics.order_performance VALUES', data_tuples)
            print("✅ Data berhasil dimuat ke ClickHouse.")
        
    except Exception as e:
        print(f"❌ Error ClickHouse: {e}")
        sys.exit(1)

    # Pembersihan
    files = glob.glob(f'{input_path}/*.csv')
    for f in files:
        os.remove(f)
    
    print("🏁 Pipeline Selesai!")

if __name__ == "__main__":
    run_orders_analytics()
