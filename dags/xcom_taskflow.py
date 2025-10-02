# xcom.py
import datetime

from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import DAG, task, dag


@task(task_id="push")
def _push(ti, ds):
    print(ds)
    ti.xcom_push(key="animal", value="cat")
    return "tiger"


@task(task_id="pull")
def _pull(ti):
    animal = ti.xcom_pull(task_ids="push", key="animal")
    print(f"This is a {animal}!")

    another_animal = ti.xcom_pull(task_ids="push", key="return_value")
    print(f"This is a {another_animal}!")


@dag(
    start_date=datetime.datetime(2025, 10, 1),
    schedule=None,
)
def xcom_taskflow():

    start = EmptyOperator(task_id="start")

    push = _push()

    pull = _pull()

    end = EmptyOperator(task_id="end")

    start >> push >> pull >> end


xcom_taskflow()