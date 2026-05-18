# MCI Tugas 2 : Penugasan 2 Open Recruitment Admin Lab MCI 2026


## 📝 Deskripsi Proyek
Proyek ini mengimplementasikan data pipeline end-to-end untuk mengambil data pesanan (orders) dari API eksternal, mengolahnya menggunakan Apache Spark untuk mendapatkan insight bisnis, menyimpannya ke ClickHouse Data Warehouse, dan memvisualisasikannya di Metabase.

## 🏗️ Arsitektur Pipeline
1. **Ingestion (Python/Requests):** Mengambil data JSON dari `http://96.9.212.102:8000/orders`, melakukan flattening data (order-product), dan menyimpannya ke format Parquet di Local Data Lake.
2. **Orchestration (Apache Airflow):** Menjadwalkan dan mengelola eksekusi task ingestion dan processing.
3. **Processing (Apache Spark):** Membaca data Parquet, melakukan agregasi (Top Products, Department Stats), dan memuat hasilnya ke ClickHouse.
4. **Storage (ClickHouse):** Menyimpan data hasil olahan dalam tabel yang dioptimalkan untuk query analitik.
5. **Visualization (Metabase):** Dashboard interaktif untuk menampilkan metrik utama bisnis.

## 📂 Struktur Folder
- `dags/`: Berisi definisi Airflow DAG (`orders_pipeline.py`).
- `scripts/`: Berisi script Python untuk ingestion (`fetch_orders.py`) dan spark processing (`process_orders.py`).
- `sql/`: Berisi DDL untuk schema ClickHouse dan contoh query SQL untuk Metabase.

## 🚀 Cara Menjalankan
1. Pastikan infrastruktur Docker (Airflow, ClickHouse, Metabase) sudah berjalan menggunakan `docker-compose.yml`.
2. Salin file dari folder `task2_orders/dags/` ke folder `dags/` utama project Anda.
3. Salin file dari folder `task2_orders/scripts/` ke folder `dags/scripts/` utama project Anda.
4. Airflow akan mendeteksi DAG baru bernama `mci_orders_pipeline`.
5. Trigger DAG secara manual atau tunggu sesuai jadwal.
6. Buka Metabase (port 3000), hubungkan ke ClickHouse, dan gunakan query di folder `sql/` untuk membuat visualisasi.

---
*Dibuat untuk Tugas Oprec MCI 2026 oleh Kelompok 29*

<img width="1445" height="752" alt="image" src="https://github.com/user-attachments/assets/3ac720e1-a71d-46ba-b308-1004c710124d" />
<img width="1333" height="795" alt="image" src="https://github.com/user-attachments/assets/82924035-5c96-4149-b706-80f1afd351a3" />
<img width="1321" height="696" alt="image" src="https://github.com/user-attachments/assets/d649e085-eb10-468f-9374-bd0c51a7d6c5" />

