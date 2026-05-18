from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'mmds_engineer',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

with DAG(
    'mci_orders_pipeline',
    default_args=default_args,
    schedule_interval='@hourly',
    catchup=False,
    description='Pipeline for Ingesting and Processing Orders Data'
) as dag:

    # Task 1: Ingest data dari API Orders
    ingest_orders = BashOperator(
        task_id='fetch_orders_from_api',
        # Asumsi script diletakkan di dags/scripts dalam container
        bash_command='python /opt/airflow/dags/scripts/fetch_orders.py'
    )

    # Task 2: Process data dengan Spark dan simpan ke ClickHouse
    process_orders = BashOperator(
        task_id='process_orders_spark',
        bash_command='python /opt/airflow/dags/scripts/process_orders.py'
    )

    ingest_orders >> process_orders
