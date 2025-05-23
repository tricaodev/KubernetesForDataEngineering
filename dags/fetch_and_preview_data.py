from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta, timezone
import pandas as pd
import requests

def get_data(**kwargs):
    url = "https://raw.githubusercontent.com/airscholar/ApacheFlink-SalesAnalytics/main/output/new-output.csv"
    response = requests.get(url)

    if response.status_code == 200:
        df = pd.read_csv(url, header=None, names=['Category', 'Price', 'Quantity'])
        json_data = df.to_json(orient='records')
        kwargs['ti'].xcom_push(key='data', value=json_data)
    else:
        raise f"Failed to get data, HTTP status code: {response.status_code}"


def preview_data(**kwargs):
    json_data = kwargs['ti'].xcom_pull(key='data')
    df = pd.DataFrame(json_data)
    df['Total'] = df['Price'] * df['Quantity']
    df.groupby('Category').agg({'Price': 'sum', 'Quantity': 'sum', 'Total': 'sum'})

    print(df[['Category', 'Total']])

default_args = {
    'owner': 'tricao',
    'start_date': datetime(2025,5,23, tzinfo=timezone(timedelta(hours=7)))
}

dag = DAG(
    dag_id="fetch_and_preview_data",
    default_args=default_args,
    schedule=timedelta(days=1),
    catchup=False,
    is_paused_upon_creation=False
)

get_data = PythonOperator(
    dag=dag,
    task_id="get_data",
    python_callable=get_data
)

preview_data = PythonOperator(
    dag=dag,
    task_id="preview_data",
    python_callable=preview_data
)

get_data >> preview_data