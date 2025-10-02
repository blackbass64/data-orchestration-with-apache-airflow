import datetime

from airflow.sdk import task, DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook


with DAG(
    dag_id="check_vault_connection",
    start_date=datetime.datetime(2025, 10, 1),
    schedule=None,
    tags=["demo", "vault", "connections"],
):

    @task
    def list_tables():
        hook = PostgresHook(postgres_conn_id="my_postgres_connection")
        tables = hook.get_records(
            "SELECT table_name FROM information_schema.tables WHERE table_schema='public';"
        )
        print(tables)
        return tables
    
    list_tables()
