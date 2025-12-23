from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import json
import psycopg2
from psycopg2.extras import RealDictCursor

args = {
    "owner" : "airflow",
    "depends_on_past" : False,
    "retries" : 2,
    "retry_delay" : timedelta(minutes=5)
}

def get_cities_from_db():
    connection = psycopg2.connect(
        host = "postgres",
        database = "weather_db",
        user = "airflow",
        password = "airflow"
    )

    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT id, name, latitude, longitude FROM cities")

    cities = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return cities

def get_data_from_city(city):
    url = "https://api.open-meteo.com/v1/forecast"
    parameters = {
        "latitude" : city["latitude"],
        "longitude" : city["longitude"],
        "hourly" : "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
        "timezone" : "auto",
        "forecast_days" : 1
    }

    response = requests.get(url, params = parameters, timeout=10)
    response.raise_for_status()
    return response.json()

def extract_data_all_cities(**context):

    cities = get_cities_from_db()

    all_data = []

    for city in cities:
        try:
            city_data = get_data_from_city(city)
            all_data.append({
                "city_id": city["id"],
                "city_name": city["name"],
                "data" : city_data,
                "success": True
            })
        except Exception as e:
            all_data.append({
                "city_id": city["id"],
                "city_name": city["name"],
                "error": str(e),
                "success": False
            })

    context["ti"].xcom_push(key="data", value = all_data)
    return all_data

def load_to_db(**context):
    all_data = context['ti'].xcom_pull(
        task_ids = "extract_weather_data",
        key = "data",
    )

    connection = psycopg2.connect(
        host = "postgres",
        database = "weather_db",
        user = "airflow",
        password = "airflow"
    )

    if not all_data:
        return "No data"

    cursor = connection.cursor()

    for city_data in all_data:
        if city_data["success"]:
            cursor.execute("INSERT INTO weather_raw (city_id, data) values (%s, %s)", (city_data["city_id"] , json.dumps(city_data["data"]) ))

    connection.commit()
    cursor.close()
    connection.close()

    return

with DAG(
    dag_id = "download_and_insert_dag",
    default_args = args,
    start_date = datetime(2024,1,1),
    schedule="@daily",
    catchup = False,
    tags = ["weather", "etl"]
) as dag:
    
    extract_task = PythonOperator(
        task_id = "extract_weather_data",
        python_callable = extract_data_all_cities,
        provide_context = True
    )

    load_task = PythonOperator(
        task_id = "load_weather_data",
        python_callable = load_to_db,
        provide_context = True
    )

    extract_task >> load_task