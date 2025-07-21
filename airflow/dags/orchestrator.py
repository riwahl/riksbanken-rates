import sys
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from datetime import datetime, timedelta

sys.path.append("/opt/airflow/api-request")
from insert_records import main

default_args = {
    "description": "Orchestrator DAG for Riksbanken Rates",
    "start_date": datetime(2023, 10, 1),
    "catchup": False,
}

dag = DAG(
    dag_id="riksbanken-rates-dbt-orchestrator",
    default_args=default_args,
    schedule=timedelta(days=1),
)

with dag:
    task1 = PythonOperator(
        task_id="ingest_data_task",
        python_callable=main,
    )
    task2 = DockerOperator(
        task_id="transform_data_task",
        image="ghcr.io/dbt-labs/dbt-postgres:1.9.latest",
        command="run",
        working_dir="/usr/app",
        mounts=[
            Mount(
                source="/home/rikar/repos/riksbanken-rates/dbt/riksbanken_rates",
                target="/usr/app",
                type="bind",
            ),
            Mount(
                source="/home/rikar/repos/riksbanken-rates/dbt/profiles.yml",
                target="/root/.dbt/profiles.yml",
                type="bind",
            ),
        ],
        network_mode="riksbanken-rates_my-network",
        docker_url="unix://var/run/docker.sock",
        auto_remove="success",
    )

    task1 >> task2
