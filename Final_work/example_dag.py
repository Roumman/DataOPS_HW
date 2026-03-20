"""Пример DAG для проверки работы Airflow."""
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator


def print_hello():
    print("Hello from DataOps Final Homework!")


with DAG(
    dag_id="example_final_dag",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["final", "example"],
) as dag:
    start = EmptyOperator(task_id="start")
    process = PythonOperator(
        task_id="process",
        python_callable=print_hello,
    )
    end = EmptyOperator(task_id="end")

    start >> process >> end
