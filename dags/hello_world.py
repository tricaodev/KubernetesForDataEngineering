from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timezone, timedelta

default_args = {
    'owner': 'tricao',
    'start_date': datetime(2025, 5, 23, tzinfo=timezone(timedelta(hours=7)))
}

dag = DAG(
    dag_id="hello_world",
    default_args=default_args,
    schedule=timedelta(days=1),
    catchup=False,
    is_paused_upon_creation=False
)

t1 = BashOperator(
    dag=dag,
    task_id="hello_world",
    bash_command="echo 'Hello World'"
)

t2 = BashOperator(
    dag=dag,
    task_id="hello_owner",
    bash_command=f"echo 'Hello {default_args['owner']}'"
)

t1 >> t2