from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 12, 20),
}

with DAG(
    dag_id="dbt_marts",
    description="Run dbt marts for ticket triage analytics",
    default_args=default_args,
    schedule_interval=timedelta(seconds=4),
    catchup=False,
) as dag:
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="dbt run --profiles-dir /dbt --project-dir /dbt",
    )
