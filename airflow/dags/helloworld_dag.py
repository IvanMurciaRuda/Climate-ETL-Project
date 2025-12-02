from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id = "helloworld",
    start_date = datetime(2024,1,1),
    schedule="@daily",
    catchup = False,
    tags = ["training"]
) as dag:
    
    task1 = BashOperator(
        task_id = "hello_task_1",
        bash_command = "echo 'Hello from Airflow task 1'"
    )

    task2 = BashOperator(
        task_id = "hello_task_2",
        bash_command = "echo 'Hello from Airflow task 2'"
    )

    task1 >> task2