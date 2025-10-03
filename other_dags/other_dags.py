# my_first_dag.py
import datetime

from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.sdk import DAG

with DAG(
    dag_id="other_dags",
    start_date=datetime.datetime(2025, 10, 1),
    schedule=None,
):
    task_1 = EmptyOperator(task_id="task_1")
    task_2 = EmptyOperator(task_id="task_2")

    task_1 >> task_2