from __future__ import annotations

from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from ml.retrain import export_training_data, retrain_baseline


def refresh_dashboard() -> None:
    print("Dashboard refresh complete")


with DAG(
    dag_id="nightly_retrain_and_refresh",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["traffic", "ml", "analytics"],
) as dag:
    export_task = PythonOperator(task_id="export_training_data", python_callable=export_training_data)
    retrain_task = PythonOperator(
        task_id="retrain_baseline",
        python_callable=lambda: retrain_baseline("ml/artifacts/training_events.csv"),
    )
    refresh_task = PythonOperator(task_id="refresh_dashboard", python_callable=refresh_dashboard)

    export_task >> retrain_task >> refresh_task
