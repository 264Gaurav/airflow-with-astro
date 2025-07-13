# Overview

Welcome to Astronomer! This project was generated after you ran 'astro dev init' using the Astronomer CLI. This readme describes the contents of the project, as well as how to run Apache Airflow on your local machine.

# Project Contents

Your Astro project contains the following files and folders:

- dags: This folder contains the Python files for your Airflow DAGs. By default, this directory includes one example DAG:
  - `example_astronauts`: This DAG shows a simple ETL pipeline example that queries the list of astronauts currently in space from the Open Notify API and prints a statement for each astronaut. The DAG uses the TaskFlow API to define tasks in Python, and dynamic task mapping to dynamically print a statement for each astronaut. For more on how this DAG works, see our [Getting started tutorial](https://www.astronomer.io/docs/learn/get-started-with-airflow).
- Dockerfile: This file contains a versioned Astro Runtime Docker image that provides a differentiated Airflow experience. If you want to execute other commands or overrides at runtime, specify them here.
- include: This folder contains any additional files that you want to include as part of your project. It is empty by default.
- packages.txt: Install OS-level packages needed for your project by adding them to this file. It is empty by default.
- requirements.txt: Install Python packages needed for your project by adding them to this file. It is empty by default.
- plugins: Add custom or community plugins for your project to this file. It is empty by default.
- airflow_settings.yaml: Use this local-only file to specify Airflow Connections, Variables, and Pools instead of entering them in the Airflow UI as you develop DAGs in this project.

# Deploy Your Project Locally

### Start Airflow on your local machine by running 'astro dev start'. and Stop by 'astro dev stop'

This command will spin up five Docker containers on your machine, each for a different Airflow component:

- Postgres: Airflow's Metadata Database
- Scheduler: The Airflow component responsible for monitoring and triggering tasks
- DAG Processor: The Airflow component responsible for parsing DAGs
- API Server: The Airflow component responsible for serving the Airflow UI and API
- Triggerer: The Airflow component responsible for triggering deferred tasks

When all five containers are ready the command will open the browser to the Airflow UI at http://localhost:8080/. You should also be able to access your Postgres Database at 'localhost:5432/postgres' with username 'postgres' and password 'postgres'.

Note: If you already have either of the above ports allocated, you can either [stop your existing Docker containers or change the port](https://www.astronomer.io/docs/astro/cli/troubleshoot-locally#ports-are-not-available-for-my-local-airflow-webserver).

# ETL Weather Pipeline

This project is an ETL (Extract, Transform, Load) pipeline built using Apache Airflow. The pipeline fetches weather data for a specific location (London) from the Open-Meteo API and processes it for further use.

## Features

- **Extract**: Fetch weather data from the Open-Meteo API.
- **Transform**: Process and clean the weather data.
- **Load**: Store the processed data into a PostgreSQL database.

## Prerequisites

- Python 3.7+
- Apache Airflow
- PostgreSQL database
- Open-Meteo API access

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd etlWeather
   ```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up Airflow:

```bash
export AIRFLOW_HOME=~/airflow
airflow db init
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com
```

4. Configure Airflow connections:

   1. Add a connection for PostgreSQL (postgres_default).
   2. Add a connection for the Open-Meteo API (open_meteo_api).

## Configuration

    1. Update the LATITUDE and LONGITUDE variables in etlWeather.py to specify the desired location.
    2. Ensure the POSTGRES_CONN_ID and API_CONN_ID match the Airflow connection IDs.

# Deploy Your Project to Astronomer

If you have an Astronomer account, pushing code to a Deployment on Astronomer is simple. For deploying instructions, refer to Astronomer documentation: https://www.astronomer.io/docs/astro/deploy-code/
