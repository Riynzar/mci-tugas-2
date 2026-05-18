import requests
import pandas as pd
import os
from datetime import datetime
import sys

def fetch_orders_data():
    print("🚀 Memulai proses pengambilan data dari API Orders...")
    url = "http://96.9.212.102:8000/orders"
    
    headers = {
        "User-Agent": "MCI-Task2-Agent/1.0",
        "Accept": "application/json"
    }
    
    try:
        print(f"📡 Menghubungi URL: {url} ...")
        response = requests.get(url, headers=headers, timeout=60)
        
        if response.status_code != 200:
            print(f"❌ Error HTTP: Status {response.status_code}")
            response.raise_for_status()
            
        print("✅ Koneksi berhasil, memproses JSON...")
        data = response.json()
        orders = data.get('orders', [])
        
        if not orders:
            print("⚠️ Peringatan: Data orders kosong!")
            return

        flattened_data = []
        for order in orders:
            base_order_info = {
                'order_id': order.get('order_id'),
                'user_id': order.get('user_id'),
                'order_number': order.get('order_number'),
                'order_dow': order.get('order_dow'),
                'order_hour_of_day': order.get('order_hour_of_day'),
                'days_since_prior_order': order.get('days_since_prior_order'),
            }
            
            for product in order.get('products', []):
                product_info = {
                    'product_id': product.get('product_id'),
                    'product_name': product.get('product_name'),
                    'aisle': product.get('aisle'),
                    'department': product.get('department'),
                    'reordered': product.get('reordered')
                }
                combined = {**base_order_info, **product_info}
                flattened_data.append(combined)
            
        df = pd.DataFrame(flattened_data)
        
        # MENGGUNAKAN CSV UNTUK STABILITAS VERSI
        output_dir = '/opt/airflow/data_lake/orders'
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f'{output_dir}/orders_{current_time}.csv'
        
        os.makedirs(output_dir, exist_ok=True)
        print(f"📝 Menyimpan {len(df)} baris ke: {output_path}")
        df.to_csv(output_path, index=False)
        
        print(f"✅ Sukses menyimpan CSV!")

    except Exception as e:
        print(f"❌ Terjadi kesalahan: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    fetch_orders_data()
