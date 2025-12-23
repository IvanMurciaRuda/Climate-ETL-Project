from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from psycopg2.extras import RealDictCursor

import logging
import psycopg2
import json
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'plugins'))
logger = logging.getLogger(__name__)

from transform import WeatherTransform

args = {
    "owner" : "airflow",
    "depends_on_past" : False,
    "retries" : 2,
    "retry_delay" : timedelta(minutes=5)
}

def extract_raw_data(**context):
    connection = psycopg2.connect(
        host = "postgres",
        database = "weather_db",
        user = "airflow",
        password = "airflow"
    )

    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT wr.city_id, wr.data as raw_json, c.name as city_name from weather_raw as wr join cities c on wr.city_id = c.id WHERE wr.extracted_at >= NOW() - INTERVAL '1 DAY'")

    data = cursor.fetchall()

    formatted_data = []

    for row in data:
        formatted_data.append({
            "city_id" : row['city_id'],
            "city_name" : row['city_name'],
            "raw_json" : row['raw_json']
        })

    logger.info(f"Extracted {len(formatted_data)} registers of raw data")

    context['ti'].xcom_push(key='raw_data', value=formatted_data)

    cursor.close()
    connection.close()

    return formatted_data

def transform_data(**context):

    raw_data = context['ti'].xcom_pull(task_ids = 'extract_task', key='raw_data')

    if not raw_data:
        logger.warning("No data extracted from database")
        return []

    transformer = WeatherTransform()

    transformed_data = transformer.extract_hourly_records(raw_data)

    if not transformed_data:
        logger.warning("No data transformed")
        return []

    logger.info(f"transformed {len(transformed_data)} rows of data")        

    return transformed_data

def load_to_processed(**context):
    # 1. Obtener datos transformados de XCom
    # 2. Conectar a PostgreSQL
    # 3. INSERT INTO weather_processed ... ON CONFLICT DO UPDATE
    # 4. Loggear cuántos registros se insertaron/actualizaron
    return

with DAG(
    dag_id = "transform_weather_dag",
    default_args = args,
    start_date = datetime(2024,1,1),
    schedule="@daily",
    catchup = False,
    tags = ["weather", "etl"]
) as dag:
    extract_task = PythonOperator(
        task_id = "extract_task",
        python_callable = extract_raw_data,
        provide_context = True
    )

    transform_task = PythonOperator(
        task_id = "transform_task",
        python_callable = transform_data,
        provide_context = True
    )

    extract_task >> transform_task