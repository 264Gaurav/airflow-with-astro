from airflow import DAG
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task
# from airflow.utils.dates import days_ago
from datetime import datetime
import requests
import json

# Latitude and longitude for the desired location (London in this case)
LATITUDE = '51.5074'
LONGITUDE = '-0.1278'
POSTGRES_CONN_ID='postgres_default'
API_CONN_ID='open_meteo_api'

default_args={
    'owner':'airflow',
    'start_date':datetime(2025, 7, 1),
}

## DAG
with DAG(dag_id='weather_etl_pipeline',
         default_args=default_args,
         schedule='@daily',
         catchup=False) as dags:

    @task()
    def extract_weather_data():
        """Extract weather data from Open-Meteo API using Airflow Connection."""

        # Use HTTP Hook to get connection details from Airflow connection

        http_hook=HttpHook(http_conn_id=API_CONN_ID,method='GET')

        ## Build the API endpoint
        ## https://api.open-meteo.com/v1/forecast?latitude=51.5074&longitude=-0.1278&current_weather=true
        endpoint=f'/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current_weather=true'

        ## Make the request via the HTTP Hook
        response=http_hook.run(endpoint)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch weather data: {response.status_code}")

    @task()
    def transform_weather_data(weather_data):
        """Transform the extracted weather data."""
        current_weather = weather_data['current_weather']
        transformed_data = {
            'latitude': LATITUDE,
            'longitude': LONGITUDE,
            'temperature': current_weather['temperature'],
            'windspeed': current_weather['windspeed'],
            'winddirection': current_weather['winddirection'],
            'weathercode': current_weather['weathercode']
        }
        return transformed_data

    @task()
    def load_weather_data(transformed_data):
        """Load transformed data into PostgreSQL."""
        pg_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
        conn = pg_hook.get_conn()
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            latitude FLOAT,
            longitude FLOAT,
            temperature FLOAT,
            windspeed FLOAT,
            winddirection FLOAT,
            weathercode INT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Insert transformed data into the table
        cursor.execute("""
        INSERT INTO weather_data (latitude, longitude, temperature, windspeed, winddirection, weathercode)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            transformed_data['latitude'],
            transformed_data['longitude'],
            transformed_data['temperature'],
            transformed_data['windspeed'],
            transformed_data['winddirection'],
            transformed_data['weathercode']
        ))

        conn.commit()
        cursor.close()

    ## DAG Worflow- ETL Pipeline
    weather_data= extract_weather_data()
    transformed_data=transform_weather_data(weather_data)
    load_weather_data(transformed_data)





































# from airflow import DAG
# from airflow.decorators import task
# from airflow.providers.http.hooks.http import HttpHook
# from airflow.providers.postgres.hooks.postgres import PostgresHook
# from airflow.utils import timezone
# from datetime import timedelta

# # Location & connections
# LATITUDE = '51.5074'
# LONGITUDE = '-0.1278'
# API_CONN_ID = 'open_meteo_api'
# POSTGRES_CONN_ID = 'postgres_default'

# default_args = {
#     'owner': 'airflow',
#     'retries': 1,
#     'retry_delay': timedelta(minutes=5),
# }

# with DAG(
#     dag_id='weather_etl_pipeline',
#     default_args=default_args,
#     start_date=timezone.datetime(2025, 7, 1),
#     schedule='@daily',
#     catchup=False,
#     tags=['weather', 'example'],
#     doc_md=__doc__,  # makes your module docstring show up in the UI
# ) as dag:

#     @task()
#     def extract_weather_data():
#         """Extract current weather from Open‑Meteo via HttpHook."""
#         hook = HttpHook(method='GET', http_conn_id=API_CONN_ID)
#         endpoint = f'/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current_weather=true'
#         response = hook.run(endpoint, extra_options={'timeout': 10})
#         if response.status_code != 200:
#             raise AirflowException(f"HTTP {response.status_code}: {response.text}")
#         return response.json()  # TaskFlow will XCom‑serialize this dict

#     @task()
#     def transform_weather_data(raw: dict):
#         """Pick out just the fields we care about."""
#         cw = raw['current_weather']
#         return {
#             'latitude': float(LATITUDE),
#             'longitude': float(LONGITUDE),
#             'temperature': cw['temperature'],
#             'windspeed': cw['windspeed'],
#             'winddirection': cw['winddirection'],
#             'weathercode': cw['weathercode'],
#         }

#     @task()
#     def load_weather_data(data: dict):
#         """Insert our transformed data into Postgres."""
#         pg = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
#         insert_sql = """
#             INSERT INTO weather_data
#             (latitude, longitude, temperature, windspeed, winddirection, weathercode)
#             VALUES (%s, %s, %s, %s, %s, %s);
#         """
#         pg.run(insert_sql, parameters=(
#             data['latitude'],
#             data['longitude'],
#             data['temperature'],
#             data['windspeed'],
#             data['winddirection'],
#             data['weathercode'],
#         ))

#         # Note: pg.run will open, commit, and close its own cursor.

#     # Define pipeline
#     raw = extract_weather_data()
#     clean = transform_weather_data(raw)
#     load_weather_data(clean)

