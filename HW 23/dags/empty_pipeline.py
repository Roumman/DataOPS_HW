#airflow
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="empty_pipeline_hw23",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    tags=["hw23", "empty"],
    catchup=False,
) as dag:
    task_start = BashOperator(
        task_id="start",
        bash_command='echo "Задача start выполнена"',
    )
    task_process = BashOperator(
        task_id="process",
        bash_command='echo "Задача process выполнена"',
    )
    task_end = BashOperator(
        task_id="end",
        bash_command='echo "Задача end выполнена"',
    )

    task_start >> task_process >> task_end
