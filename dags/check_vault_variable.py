import datetime

from airflow.sdk import task, DAG, Variable


with DAG(
    dag_id="check_vault_variable",
    start_date=datetime.datetime(2025, 10, 1),
    schedule=None,
    tags=["demo", "vault", "variables"],
):
    @task
    def show_hello():
        val = Variable.get("hello")
        print(f"[Vault Variable] hello = {val}")

    show_hello()

